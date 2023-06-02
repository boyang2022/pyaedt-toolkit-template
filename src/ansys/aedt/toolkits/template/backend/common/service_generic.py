import os

import psutil
import pyaedt

from ansys.aedt.toolkits.template.backend.common.logger_handler import logger
from ansys.aedt.toolkits.template.backend.common.properties import properties
from ansys.aedt.toolkits.template.backend.common.thread_manager import ThreadManager

thread = ThreadManager()


class ServiceGeneric(object):
    """Generic backend class. It provides basic functions to control AEDT and properties
    to share between backend and frontend.

    Examples
    --------
    >>> import time
    >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
    >>> service = ToolkitService()
    >>> properties = service.get_properties()
    >>> new_properties = {"aedt_version": "2022.2"}
    >>> service.set_properties(new_properties)
    >>> new_properties = service.get_properties()
    >>> msg = service.launch_aedt()
    >>> response = service.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = service.get_thread_status()
    >>> service.release_desktop()

    """

    def __init__(self):
        self.desktop = None
        self.aedtapp = None

    @staticmethod
    def set_properties(data):
        """Assign the passed data to the internal data model.

        Parameters
        ----------
        data : dict
            The dictionary containing the properties to be updated.

        Returns
        -------
        tuple[bool, str]
            A tuple indicating the success status and a message.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.set_properties({"property1": value1, "property2": value2})

        """

        logger.debug("Updating the internal properties.")
        if data:
            try:
                for key in data:
                    setattr(properties, key, data[key])
                msg = "properties updated successfully"
                logger.debug(msg)
                return True, msg
            except:
                return False, "Frozen property access"
        else:
            msg = "body is empty!"
            logger.debug(msg)
            return False, msg

    @staticmethod
    def get_properties():
        """Get toolkit properties.

        Returns
        -------
        dict
            The dictionary containing the toolkit properties.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.get_properties()
        {"property1": value1, "property2": value2}
        """
        return properties.export_to_dict()

    @staticmethod
    def get_thread_status():
        """Get toolkit thread status.

        Returns
        -------
        bool
            ``True`` when active, ``False`` when not active.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.get_thread_status()
        """
        thread_running = thread.is_thread_running()
        is_toolkit_busy = properties.is_toolkit_busy
        if thread_running and is_toolkit_busy:  # pragma: no cover
            msg = "Backend running"
            logger.debug(msg)
            return 0, msg
        elif (not thread_running and is_toolkit_busy) or (thread_running and not is_toolkit_busy):  # pragma: no cover
            msg = "Backend crashed"
            logger.error(msg)
            return 1, msg
        else:
            msg = "Backend free"
            logger.debug(msg)
            return -1, msg

    def aedt_connected(self):
        """Check if AEDT is connected.

        Returns
        -------
        tuple[bool, str]
            A tuple indicating the connection status and a message.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.aedt_connected()
        (True, "Toolkit connected to process <process_id> on Grpc <grpc_port>")
        """
        if self.desktop:
            if self.desktop.port != 0:
                msg = "Toolkit connected to process {} on Grpc {}".format(
                    str(self.desktop.aedt_process_id),
                    str(self.desktop.port),
                )
                logger.debug(msg)
            else:
                msg = "Toolkit connected to process {}".format(str(self.desktop.aedt_process_id))
                logger.debug(msg)
            connected = True
        else:
            msg = "Toolkit not connected to AEDT"
            logger.debug(msg)
            connected = False
        return connected, msg

    @staticmethod
    def installed_aedt_version():
        """
        Return the installed AEDT versions.

        Returns
        -------
        list
            List of installed AEDT versions.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.installed_aedt_version()
        ["2021.1", "2021.2", "2022.1"]
        """

        # Detect existing AEDT installation
        installed_versions = []
        for ver in pyaedt.misc.list_installed_ansysem():
            installed_versions.append(
                "20{}.{}".format(ver.replace("ANSYSEM_ROOT", "")[:2], ver.replace("ANSYSEM_ROOT", "")[-1])
            )
        logger.debug(str(installed_versions))
        return installed_versions

    @staticmethod
    def aedt_sessions():
        """Get information for the active AEDT sessions.

        Returns
        -------
        list
            List of AEDT PIDs.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.aedt_sessions()
        [[pid1, grpc_port1], [pid2, grpc_port2]]
        """
        if not properties.is_toolkit_busy:
            version = properties.aedt_version
            keys = ["ansysedt.exe"]
            if version and "." in version:
                version = version[-4:].replace(".", "")
            if version < "222":  # pragma: no cover
                version = version[:2] + "." + version[2]
            sessions = []
            for p in psutil.process_iter():
                try:
                    if p.name() in keys:
                        cmd = p.cmdline()
                        if not version or (version and version in cmd[0]):
                            if "-grpcsrv" in cmd:
                                if not version or (version and version in cmd[0]):
                                    try:
                                        sessions.append(
                                            [
                                                p.pid,
                                                int(cmd[cmd.index("-grpcsrv") + 1]),
                                            ]
                                        )
                                    except IndexError:
                                        sessions.append(
                                            [
                                                p.pid,
                                                -1,
                                            ]
                                        )
                            else:
                                sessions.append(
                                    [
                                        p.pid,
                                        -1,
                                    ]
                                )
                except:
                    pass
            logger.debug(str(sessions))
            return sessions
        else:
            logger.debug("No active sessions")
            return []

    @thread.launch_thread
    def launch_aedt(self):
        """Launch AEDT. This method is launched in a thread.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> toolkit_free = service.get_thread_status()
        """

        connected, msg = self.aedt_connected()
        if not connected:
            version = properties.aedt_version
            non_graphical = properties.non_graphical
            selected_process = properties.selected_process
            use_grpc = properties.use_grpc

            pyaedt.settings.use_grpc_api = use_grpc
            if selected_process == 0:  # pragma: no cover
                # Launch AEDT with COM
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    new_desktop_session=True,
                )
            elif use_grpc:
                # Launch AEDT with GRPC
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    port=selected_process,
                    new_desktop_session=False,
                )
            else:  # pragma: no cover
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    aedt_process_id=selected_process,
                    new_desktop_session=False,
                )

            if self.desktop:
                msg = "AEDT launched"
                logger.debug(msg)
                if properties.active_project_name and not os.path.exists(
                    properties.active_project_name + ".lock"
                ):  # pragma: no cover
                    self.open_project(properties.active_project_name)

                # After launching AEDT we need to release the desktop because
                # this method is launched in a thread.
                if use_grpc:
                    new_properties = {"selected_process": self.desktop.port}
                    logger.debug("Grpc port {}".format(str(self.desktop.port)))
                else:
                    new_properties = {"selected_process": self.desktop.aedt_process_id}
                    logger.debug("Process ID {}".format(str(self.desktop.aedt_process_id)))

                oproject = self.desktop.odesktop.GetActiveProject()
                if oproject:
                    projectname = oproject.GetName()
                    project_path = self.desktop.odesktop.GetProjectDirectory()
                    new_properties["active_project_name"] = os.path.join(project_path, projectname + ".aedt")
                    active_design = oproject.GetActiveDesign()
                    logger.debug("Project name: {}".format(projectname))

                    if projectname and "active_project_name" in properties.__dir__():
                        new_properties["project_list"] = self.desktop.project_list()

                    if active_design:
                        design_name = active_design.GetName()
                        new_properties["active_design_name"] = design_name
                        logger.debug("Design name: {}".format(design_name))
                        if "active_design_name" in properties.__dir__():
                            new_properties["active_design_name"] = design_name
                            new_properties["design_list"] = self.desktop.design_list()

                self.set_properties(new_properties)

                self.desktop.release_desktop(False, False)
                logger.debug("Desktop released")
                self.desktop = None
            else:  # pragma: no cover
                msg = "AEDT launched"
                logger.error(msg)
                return False
        return True

    def connect_aedt(self):
        """Connect to an existing AEDT session. You can control the AEDT process ID with the properties.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_aedt()
        """
        if properties.selected_process == 0:
            logger.error("Process ID not defined")
            return False
        connected, msg = self.aedt_connected()
        if connected:
            self.desktop.release_desktop(False, False)

        self.desktop = None
        self.aedtapp = None
        version = properties.aedt_version
        non_graphical = properties.non_graphical
        selected_process = properties.selected_process
        use_grpc = properties.use_grpc

        pyaedt.settings.use_grpc_api = use_grpc
        logger.debug("Connecting AEDT")
        if use_grpc:
            # Launch AEDT with GRPC
            self.desktop = pyaedt.Desktop(
                specified_version=version,
                non_graphical=non_graphical,
                port=selected_process,
                new_desktop_session=False,
            )

        else:  # pragma: no cover
            self.desktop = pyaedt.Desktop(
                specified_version=version,
                non_graphical=non_graphical,
                aedt_process_id=selected_process,
                new_desktop_session=False,
            )

        if not self.desktop:
            logger.debug("AEDT not connected")
            return False

        active_project_name = properties.active_project_name
        if active_project_name != "No project" and active_project_name in self.desktop.project_list():
            oproject = self.desktop.odesktop.SetActiveProject(properties.active_project_name)
        else:
            oproject = self.desktop.odesktop.GetActiveProject()

        new_properties = {}
        if oproject:
            projectname = oproject.GetName()
            logger.debug("Project name: {}".format(projectname))
            project_path = self.desktop.odesktop.GetProjectDirectory()
            new_properties["active_project_name"] = os.path.join(project_path, projectname + ".aedt")
            active_design = properties.active_design_name
            if active_design != "No design" and active_design != "":
                active_design = oproject.SetActiveDesign(properties.active_design_name)
            else:
                active_design = oproject.GetActiveDesign()
                if not active_design and self.desktop.design_list():
                    active_design = self.desktop.design_list()[0]

            if projectname and "active_project_name" in properties.__dir__():
                new_properties["project_list"] = self.desktop.project_list()

            if active_design:
                design_name = active_design.GetName()
                new_properties["active_design_name"] = design_name
                logger.debug("Design name: {}".format(design_name))
                if "active_design_name" in properties.__dir__():
                    new_properties["active_design_name"] = design_name
                    new_properties["design_list"] = self.desktop.design_list()
        elif not self.desktop.project_list():
            project = self.desktop.odesktop.NewProject()
            new_properties["active_project_name"] = os.path.join(project.GetPath(), project.GetName() + ".aedt")
            new_properties["project_list"] = self.desktop.project_list()

        self.set_properties(new_properties)
        logger.debug("AEDT connected")
        return True

    def connect_design(self, app_name=None):
        """Connect to an application design. If a design exists,
        it takes the active project and design, if not, it creates a new design of the specified type.
        If a design name and project name is specified in the properties, it tries to connect to this design.
        If an app_name is specified the active design must have the same type, if not, it will create a new design.

        Parameters
        ----------
        app_name : str
            Aedt application name. The default is connecting to active design. Application available are:

            * Circuit
            * Hfss
            * Edb
            * Emit
            * Hfss3dLayout
            * Icepak
            * Maxwell2d
            * Maxwell3d
            * Q2d
            * Q3d
            * Rmxprt
            * Simplorer

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_design()

        """

        aedt_apps = [
            "Circuit",
            "Hfss",
            "Edb",
            "Emit",
            "Hfss3dLayout",
            "Icepak",
            "Maxwell2d",
            "Maxwell3d",
            "MaxwellCircuit",
            "Q2d",
            "Q3d",
            "Rmxprt",
            "Simplorer",
        ]

        if self.connect_aedt():
            project_name = properties.active_project_name
            design_name = properties.active_design_name

            # Take only the name
            project_name = os.path.splitext(os.path.basename(project_name))[0]

            # Check in the project if the application exists

            design_list = self.desktop.design_list()
            if design_name and design_name in design_list:
                # If the design name specified is in the project.
                aedtapp = self.desktop[[project_name, design_name]]
                design_type = type(aedtapp).__name__
                if app_name and app_name in aedt_apps and design_type != app_name:
                    aedt_app_attr = getattr(pyaedt, app_name)
                    design_name = design_name + "_" + app_name
                else:
                    aedt_app_attr = getattr(pyaedt, design_type)
            elif app_name in aedt_apps:
                design_name = pyaedt.generate_unique_name()
                aedt_app_attr = getattr(pyaedt, app_name)
            else:
                design_name = pyaedt.generate_unique_name()
                aedt_app_attr = getattr(pyaedt, "Hfss")

            self.aedtapp = aedt_app_attr(
                specified_version=properties.aedt_version,
                aedt_process_id=properties.selected_process,
                non_graphical=properties.non_graphical,
                new_desktop_session=False,
                projectname=project_name,
                designname=design_name,
            )

            if self.aedtapp:
                new_properties = {
                    "active_project_name": self.aedtapp.project_file,
                    "active_design_name": self.aedtapp.design_name,
                    "design_list": self.desktop.design_list(),
                }
                self.set_properties(new_properties)
                return True

        return False

    def release_desktop(self, close_projects=False, close_on_exit=False):
        """Release AEDT.

        Parameters
        ----------
        close_projects : bool, optional
            Whether to close the AEDT projects that are open in the session.
            The default is ``True``.
        close_on_exit : bool, optional
            Whether to close the active AEDT session on exiting AEDT.
            The default is ``True``.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.release_desktop(True, True)

        """
        released = True
        if self.desktop:
            try:
                released = self.desktop.release_desktop(close_projects, close_on_exit)
            except:
                logger.error("Desktop not released")
                return False

        if not released and self.connect_aedt():
            try:
                self.desktop.release_desktop(close_projects, close_on_exit)
                self.desktop = None
                logger.debug("Desktop released")
                return True
            except:
                logger.error("Desktop not released")
                return False
        elif released:
            return True
        else:
            logger.error("Desktop not released")
            return False

    def open_project(self, project_name=None):
        """Open AEDT project.

        Parameters
        ----------
        project_name : str, optional
            Project path to open.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.open_project("path/to/file")
        >>> service.release_desktop()

        """
        if self.desktop and project_name:
            self.desktop.odesktop.OpenProject(project_name)
            logger.debug("Project {} opened".format(project_name))
            return True
        else:
            return False

    def get_design_names(self):
        """Get design names for a specific project, the first one is the active.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.get_design_names()
        """
        if properties.selected_process == 0:
            logger.error("Process ID not defined")
            return False
        connected, msg = self.aedt_connected()
        if connected:
            self.desktop.release_desktop(False, False)

        self.desktop = None
        self.aedtapp = None
        version = properties.aedt_version
        non_graphical = properties.non_graphical
        selected_process = properties.selected_process
        use_grpc = properties.use_grpc

        pyaedt.settings.use_grpc_api = use_grpc
        logger.debug("Connecting AEDT")
        if use_grpc:
            # Launch AEDT with GRPC
            self.desktop = pyaedt.Desktop(
                specified_version=version,
                non_graphical=non_graphical,
                port=selected_process,
                new_desktop_session=False,
            )

        else:  # pragma: no cover
            self.desktop = pyaedt.Desktop(
                specified_version=version,
                non_graphical=non_graphical,
                aedt_process_id=selected_process,
                new_desktop_session=False,
            )

        if not self.desktop:
            logger.debug("AEDT not connected")
            return False
        oproject = None
        if properties.active_project_name != "No project":
            project_name = os.path.splitext(os.path.basename(properties.active_project_name))[0]
            oproject = self.desktop.odesktop.SetActiveProject(project_name)
        design_list = self.desktop.design_list()
        if design_list and oproject:
            active_design = oproject.GetActiveDesign()
            if not active_design:
                active_design = design_list[0]
            else:
                active_design = active_design.GetName()
            index = design_list.index(active_design)
            design_list.insert(0, design_list.pop(index))
        self.desktop.release_desktop(False, False)
        return design_list

    @thread.launch_thread
    def save_project(self):
        """Save project. It uses the properties to get the project path. This method is launched in a thread.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_aedt()
        >>> service.save_project()
        """
        if self.connect_aedt():
            new_project_name = properties.active_project_name
            self.desktop.save_project(project_path=new_project_name)
            self.desktop.release_desktop(False, False)
            self.desktop = None
            logger.debug("Project saved: {}".format(new_project_name))
            return True
        else:  # pragma: no cover
            logger.error("Project not saved")
            return False
