import logging

from common.global_settings import global_settings

logger = logging.getLogger(__name__)


def get_version():
    """
    return the backend version
    """
    logger.debug("Getting the version.")
    return global_settings.aedt_version
