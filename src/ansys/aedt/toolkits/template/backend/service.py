import logging

import pyaedt

logger = logging.getLogger(__name__)


def get_installed_aedt_version():
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
