from conftest import BasisTest


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_get_properties(self):
        properties = self.service.get_properties()
        assert isinstance(properties, dict)

    def test_02_set_properties(self):
        new_properties = {
            "aedt_version": self.test_config["desktopVersion"],
            "non_graphical": self.test_config["NonGraphical"],
            "use_grpc": True,
        }
        self.service.set_properties(new_properties)
        properties = self.service.get_properties()
        assert properties["aedt_version"] == self.test_config["desktopVersion"]

    def test_03_installed_aedt(self):
        versions = self.service.installed_aedt_version()
        assert isinstance(versions, list)

    def test_04_active_sessions(self):
        sessions = self.service.aedt_sessions()
        assert isinstance(sessions, list)
