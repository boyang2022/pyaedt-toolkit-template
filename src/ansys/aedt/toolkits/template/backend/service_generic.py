import logging
import os

import psutil
import pyaedt

from ansys.aedt.toolkits.template.backend.common.properties import properties
from ansys.aedt.toolkits.template.backend.common.service_aedt import RunnerDesktop

logger = logging.getLogger(__name__)
aedt_runner = RunnerDesktop()
debug = properties.debug


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
    >>> set_properties({"property1": value1, "property2": value2})
    (True, "properties updated successfully")

    """

    logger.debug("Updating the internal properties.")
    if data:
        for key in data:
            setattr(properties, key, data[key])

        return True, "properties updated successfully"
    else:
        return False, "body is empty!"


def get_properties():
    """Get toolkit properties.

    Returns
    -------
    dict
        The dictionary containing the toolkit properties.

    Examples
    --------
    >>> get_properties()
    {"property1": value1, "property2": value2}
    """
    return properties.export_to_dict()


def aedt_connected():
    """Check if AEDT is connected.

    Returns
    -------
    tuple[bool, str]
        A tuple indicating the connection status and a message.

    Examples
    --------
    >>> aedt_connected()
    (True, "AEDT connected to process <process_id> on Grpc <grpc_port>")
    """
    if aedt_runner.desktop:
        if aedt_runner.desktop.port != 0:
            return True, "AEDT connected to process {} on Grpc {}".format(
                str(aedt_runner.desktop.aedt_process_id), str(aedt_runner.desktop.port)
            )
        else:
            return True, "AEDT connected to process {}".format(
                str(aedt_runner.desktop.aedt_process_id)
            )
    else:
        return False, "AEDT not connected"


def installed_aedt_version():
    """
    Return the installed AEDT versions.

    Returns
    -------
    list
        List of installed AEDT versions.

    Examples
    --------
    >>> installed_aedt_version()
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


def aedt_sessions():
    """Get information for the active COM AEDT sessions.

    Returns
    -------
    list
        List of AEDT PIDs.

    Examples
    --------
    >>> aedt_sessions()
    [[pid1, grpc_port1], [pid2, grpc_port2]]
    """

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


def launch_aedt():
    """Launch AEDT or connect to an existing AEDT session.

    Returns
    -------
    bool
    """

    status, msg = aedt_connected()

    if status:
        return msg

    aedt_runner.launch_aedt(
        properties.aedt_version,
        properties.non_graphical,
        properties.selected_process,
        properties.use_grpc,
    )
    if (
        aedt_runner.desktop is not None
        and aedt_runner.desktop.aedt_version_id == properties.aedt_version
    ):
        if aedt_runner.desktop.port != 0:
            return "AEDT connected to process {} on Grpc {}".format(
                str(aedt_runner.desktop.aedt_process_id), str(aedt_runner.desktop.port)
            )
        else:
            return "AEDT connected to process {}".format(str(aedt_runner.desktop.aedt_process_id))
    else:
        return False


def release_desktop(close_projects=False, close_on_exit=False):
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
    """

    if aedt_runner.desktop is not None:
        aedt_runner.release_desktop(close_projects, close_on_exit)
    return True


def open_project():
    """Open an existing AEDT project.

    Returns
    -------
    str
    """

    if aedt_runner.desktop is not None:
        if ".lock" in properties.project_name:
            set_properties({"project_name": ""})
            return "Project locked"
        aedt_runner.open_project(properties.project_name)
        if len(aedt_runner.desktop.odesktop.GetProjects()) > 0:
            return "{} opened".format(
                os.path.splitext(os.path.basename(properties.project_name))[0]
            )
        return "Project name not correct"
    else:
        return "AEDT not connected"
