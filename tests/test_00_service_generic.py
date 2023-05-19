import requests

from conftest import BasisTest


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_get_properties(self):
        response = requests.get(self.url + "/get_properties")
        assert response.ok
        assert len(response.json()) == 14

    def test_02_set_properties(self):
        new_properties = {
            "aedt_version": self.test_config["desktopVersion"],
            "non_graphical": self.test_config["NonGraphical"],
            "use_grpc": True,
        }
        response = requests.put(self.url + "/set_properties", json=new_properties)
        assert response.ok
        new_properties = {"use_grpc": 1}
        response = requests.put(self.url + "/set_properties", json=new_properties)
        assert not response.ok
        response = requests.put(self.url + "/set_properties")
        assert not response.ok
