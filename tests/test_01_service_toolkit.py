from ansys.aedt.toolkits.template.backend.common.service_generic import ServiceGeneric
from ansys.aedt.toolkits.template.backend.service import ToolkitService
from conftest import BasisTest

test_project_name = "Test"


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.aedtapp = BasisTest.add_app(self, test_project_name)
        self.service_generic = ServiceGeneric()
        self.toolkit = ToolkitService(self.service_generic)
        process_id = self.aedtapp.odesktop.GetProcessID()
        new_properties = {
            "aedt_version": self.test_config["desktopVersion"],
            "non_graphical": self.test_config["NonGraphical"],
            "use_grpc": self.test_config["use_grpc"],
            "selected_process": int(process_id),
        }
        self.service_generic.set_properties(new_properties)

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_connect_hfss(self):
        assert not self.toolkit.connect_hfss()
        self.service_generic.launch_aedt()
        while self.service_generic.get_properties()["is_toolkit_running"]:
            pass
        assert self.toolkit.connect_hfss()

    def test_02_create_geometry(self):
        while self.service_generic.get_properties()["is_toolkit_running"]:
            pass
        assert self.toolkit.create_geometry()

        new_properties = {
            "geometry": "Sphere",
        }
        self.service_generic.set_properties(new_properties)
        while self.service_generic.get_properties()["is_toolkit_running"]:
            pass
        assert self.toolkit.create_geometry()
