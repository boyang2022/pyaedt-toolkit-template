import logging

import psutil
import pyaedt

from ansys.aedt.toolkits.template.backend.common.properties import properties
from ansys.aedt.toolkits.template.backend.common.service_aedt import RunnerDesktop
from ansys.aedt.toolkits.template.backend.common.thread_manager import ThreadManager

logger = logging.getLogger("Global")

# Create a handler and set logging level for the handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# link handler to logger
logger.addHandler(c_handler)
logging.basicConfig(level=logging.DEBUG)

thread = ThreadManager()


class ServiceGeneric(object):
    """Generic backend class. It provides basic functions to control AEDT and properties
    to share between backend and frontend.

    Examples
    --------
    >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
    >>> service = ToolkitService()
    >>> properties = service.get_properties()
    >>> new_properties = {"aedt_version": "2022.2"}
    >>> service.set_properties(new_properties)
    >>> new_properties = service.get_properties()
    >>> msg = service.launch_aedt()
    >>> service.release_desktop()

    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.aedt_runner = RunnerDesktop()
        self.debug = properties.debug

    def set_properties(self, data):
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

        self.logger.debug("Updating the internal properties.")
        if data:
            for key in data:
                setattr(properties, key, data[key])

            return True, "properties updated successfully"
        else:
            return False, "body is empty!"

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
        if thread_running and is_toolkit_busy:
            return 0, "Backend running"
        elif (not thread_running and is_toolkit_busy) or (thread_running and not is_toolkit_busy):
            return 1, "Backend crashed"
        else:
            return -1, "Backend free"

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
        (True, "Backend connected to process <process_id> on Grpc <grpc_port>")
        """
        if self.aedt_runner.desktop:
            if self.aedt_runner.desktop.port != 0:
                msg = "Backend connected to process {} on Grpc {}".format(
                    str(self.aedt_runner.desktop.aedt_process_id),
                    str(self.aedt_runner.desktop.port),
                )
                self.logger.debug(msg)
            else:
                msg = "Backend connected to process {}".format(
                    str(self.aedt_runner.desktop.aedt_process_id)
                )
                self.logger.debug(msg)
            connected = True
        else:
            msg = "Backend not connected to AEDT"
            self.logger.debug(msg)
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
                "20{}.{}".format(
                    ver.replace("ANSYSEM_ROOT", "")[:2], ver.replace("ANSYSEM_ROOT", "")[-1]
                )
            )
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
            return sessions
        else:
            return []

    @thread.launch_thread
    def launch_aedt(self):
        """Launch AEDT.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        """

        connected, msg = self.aedt_connected()
        if not connected:
            self.aedt_runner.launch_aedt(
                properties.aedt_version,
                properties.non_graphical,
                properties.selected_process,
                properties.use_grpc,
            )
            if properties.project_name:
                self.aedt_runner.open_project(properties.project_name)
        return True

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
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.release_desktop()

        """

        if self.aedt_runner.desktop is not None:
            self.aedt_runner.release_desktop(close_projects, close_on_exit)
        self.logger.debug("AEDT released")
        return True
