"""
Unit Test Configuration Module
-------------------------------

Description
===========

This module contains the configuration and fixture for the pytest-based unit tests for pyaedt.

The default configuration can be changed by placing a file called local_config.json in the same
directory as this module. An example of the contents of local_config.json
{
  "desktopVersion": "2023.1",
  "NonGraphical": false,
  "NewThread": false,
  "test_desktops": true
}

"""
import datetime
import gc
import json
import os
import shutil
import sys
import tempfile

from pyaedt import pyaedt_logger
from pyaedt import settings

settings.enable_error_handler = False
settings.enable_desktop_logs = False

import pytest

local_path = os.path.dirname(os.path.realpath(__file__))

from pyaedt import Desktop
from pyaedt.generic.filesystem import Scratch

from ansys.aedt.toolkits.template.backend.service import ToolkitService

test_project_name = "test_antenna"

sys.path.append(local_path)

# Initialize default desktop configuration
default_version = "2023.1"

config = {"desktopVersion": default_version, "NonGraphical": True, "NewThread": True}

# Check for the local config file, override defaults if found
local_config_file = os.path.join(local_path, "local_config.json")
if os.path.exists(local_config_file):
    with open(local_config_file) as f:
        local_config = json.load(f)
    config.update(local_config)

settings.use_grpc_api = config.get("use_grpc", True)
settings.non_graphical = config["NonGraphical"]

test_folder = "unit_test" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
scratch_path = os.path.join(tempfile.gettempdir(), test_folder)
if not os.path.exists(scratch_path):
    try:
        os.makedirs(scratch_path)
    except:
        pass

logger = pyaedt_logger


class BasisTest(object):
    def my_setup(self):
        self.desktop = Desktop(desktop_version, non_graphical, new_desktop_session=False)
        self.desktop.disable_autosave()
        self.test_config = config
        self.local_path = local_path
        self._main = sys.modules["__main__"]

        self.service = ToolkitService()

        new_properties = {
            "non_graphical": config["NonGraphical"],
            "aedt_version": config["desktopVersion"],
            "selected_process": int(self.desktop.aedt_process_id),
        }
        self.service.set_properties(new_properties)

        self.service.launch_aedt()

        while self.service.get_thread_status()[0] != -1:
            pass

    def my_teardown(self):
        if self.desktop:
            try:
                oDesktop = self._main.oDesktop
                proj_list = oDesktop.GetProjectList()
            except Exception as e:
                oDesktop = None
                proj_list = []
            if oDesktop and not settings.non_graphical:
                oDesktop.ClearMessages("", "", 3)
            for proj in proj_list:
                oDesktop.CloseProject(proj)
            del self.desktop

        logger.remove_all_project_file_logger()
        shutil.rmtree(scratch_path, ignore_errors=True)

    def teardown_method(self):
        """
        Could be redefined
        """
        pass

    def setup_method(self):
        """
        Could be redefined
        """
        pass


# Define desktopVersion explicitly since this is imported by other modules
desktop_version = config["desktopVersion"]
new_thread = config["NewThread"]
non_graphical = config["NonGraphical"]
local_scratch = Scratch(scratch_path)


@pytest.fixture(scope="session", autouse=True)
def desktop_init():
    desktop = Desktop(desktop_version, non_graphical, new_thread)
    new_project = desktop.odesktop.NewProject()
    desktop.save_project(
        project_name=new_project.GetName(),
        project_path=os.path.join(local_scratch.path, new_project.GetName() + ".aedt"),
    )
    yield
    desktop.release_desktop(True, True)
    del desktop
    gc.collect()
