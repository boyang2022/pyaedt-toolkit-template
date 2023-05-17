import os

from ansys.aedt.toolkits.template.backend.service import ToolkitService
from conftest import BasisTest

test_project_name = "Test"


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.aedtapp = BasisTest.add_app(self, test_project_name)
        self.service = ToolkitService()

        process_id = self.aedtapp.odesktop.GetProcessID()
        new_properties = {
            "aedt_version": self.test_config["desktopVersion"],
            "non_graphical": self.test_config["NonGraphical"],
            "use_grpc": self.test_config["use_grpc"],
            "selected_process": int(process_id),
        }
        self.service.set_properties(new_properties)
        self.service.launch_aedt()
        while self.service.get_thread_status()[0] != -1:
            pass

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_connect_hfss(self):
        assert self.service.connect_hfss()

    def test_02_create_geometry(self):
        assert self.service.create_geometry()
        while self.service.get_thread_status()[0] != -1:
            pass

        new_properties = {
            "geometry": "Sphere",
        }
        self.service.set_properties(new_properties)

        assert self.service.create_geometry()
        while self.service.get_thread_status()[0] != -1:
            pass

    def test_03_save_project(self):
        while self.service.get_thread_status()[0] != -1:
            pass

        new_properties = {
            "new_project_name": os.path.join(self.aedtapp.project_path, "new.aedt"),
        }
        self.service.set_properties(new_properties)

        assert self.service.save_project()
        while self.service.get_thread_status()[0] != -1:
            pass
