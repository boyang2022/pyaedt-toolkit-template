import os

import ansys.aedt.toolkits.template.backend.service_generic as service_generic
from conftest import BasisTest

test_project_name = "Test"
test_subfolder = "T00"


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.aedtapp = BasisTest.add_app(self, test_project_name)

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_get_properties(self):
        properties = service_generic.get_properties()
        assert isinstance(properties, dict)

    def test_02_set_properties(self):
        new_properties = {
            "aedt_version": self.test_config["desktopVersion"],
            "non_graphical": self.test_config["NonGraphical"],
            "use_grpc": self.test_config["use_grpc"],
        }
        service_generic.set_properties(new_properties)
        properties = service_generic.get_properties()
        assert properties["aedt_version"] == self.test_config["desktopVersion"]

    def test_03_installed_aedt(self):
        versions = service_generic.installed_aedt_version()
        assert isinstance(versions, list)

    def test_04_active_sessions(self):
        sessions = service_generic.aedt_sessions()
        assert isinstance(sessions, list)
        assert len(sessions) == 1

    def test_05_open_project(self):
        filename = os.path.join(self.local_path, "example_models", test_subfolder, "Coax_HFSS.aedt")
        new_properties = {
            "project_name": filename,
        }
        service_generic.set_properties(new_properties)
        assert service_generic.open_project() == "AEDT not connected"

        process_id = self.aedtapp.odesktop.GetProcessID()
        new_properties = {"use_grpc": True, "selected_process": process_id}
        service_generic.set_properties(new_properties)
        msg = service_generic.launch_aedt()
        assert str(process_id) in msg

        new_properties = {
            "project_name": filename,
        }
        service_generic.set_properties(new_properties)
        service_generic.open_project()
        assert len(self.aedtapp.odesktop.GetProjects()) > 0

        filename = os.path.join(
            self.local_path, "example_models", test_subfolder, "Coax_HFSS_locked.aedt.lock"
        )
        new_properties = {
            "project_name": filename,
        }
        service_generic.set_properties(new_properties)
        assert service_generic.open_project() == "Project locked"
