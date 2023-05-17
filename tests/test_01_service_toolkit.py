import os

from conftest import BasisTest

test_project_name = "Test"


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_connect_hfss(self):
        assert self.service.connect_hfss()

    def test_01_create_geometry(self):
        assert self.service.create_geometry()
        while self.service.get_thread_status()[0] != -1:
            pass
        assert len(self.service.comps) == 1
        new_properties = {
            "geometry": "Sphere",
        }
        self.service.set_properties(new_properties)

        assert self.service.create_geometry()
        while self.service.get_thread_status()[0] != -1:
            pass
        assert len(self.service.comps) == 2

    def test_03_save_project(self):
        new_properties = {
            "new_project_name": os.path.join(self.service.aedtapp.project_path, "new.aedt"),
        }
        self.service.set_properties(new_properties)

        assert self.service.save_project()
        while self.service.get_thread_status()[0] != -1:
            pass
