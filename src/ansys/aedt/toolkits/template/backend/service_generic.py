import logging

from common.properties import properties
import psutil
import pyaedt

logger = logging.getLogger(__name__)


def set_properties(data):
    """Assign the passed data to the internal data model.

    Parameters
    ----------
    data : dict

    Returns
    -------
    bool
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
        Properties.
    """
    return properties.export_to_dict()


def installed_aedt_version():
    """
    return the backend version
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
    """
    version = properties.aedt_version
    keys = ["ansysedt.exe"]
    if version and "." in version:
        version = version[-4:].replace(".", "")
    if version < "222":
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


def new_aedt(version, non_graphical):
    pyaedt.settings.use_grpc_api = True
    if version not in get_installed_aedt_version():
        logger.info("Incorrect version")
        return False
    aedtapp = pyaedt.Desktop(
        specified_version=version,
        non_graphical=non_graphical,
        new_desktop_session=True,
    )
    return aedtapp
