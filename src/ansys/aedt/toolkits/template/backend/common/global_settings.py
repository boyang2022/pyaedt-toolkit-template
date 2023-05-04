import os

# from common.properties import properties


class GlobalSettings(object):
    """
    Class to define the global settings.
    """

    def __init__(self):
        # set current installation folder
        self.install_path = os.path.normpath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
        )

        # from user_config.json file
        user_config_fullname = os.path.join(self.install_path, "user_config.json")
        self.read_options_from_default_file(user_config_fullname)

    def read_options_from_default_file(self, filefullname):
        x = 1


def get_aedt_env_var(version):
    return "ANSYSEM_ROOT" + str(version).replace(".", "")[-3:]


global_settings = GlobalSettings()
