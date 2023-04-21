from ansys.aedt.toolkits.template.backend.template_script import TemplateBackend
from conftest import BasisTest

test_project_name = "Template_test"


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.aedtapp = BasisTest.add_app(self, test_project_name)
        self.template = TemplateBackend(self.aedtapp)

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_draw_box(self):
        self.template.multiplier = 5.0
        box = self.template.draw_box()
        assert box.volume - 124.99999999999993 < 1e-6

    def test_02_draw_sphere(self):
        sp = self.template.draw_sphere()
        assert sp.volume - 523.5987755982989 < 1e-6
