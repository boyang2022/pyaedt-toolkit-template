import numpy as np
from pyaedt import Desktop
from pyaedt import Hfss
from pyaedt.generic.general_methods import pyaedt_function_handler


class ToolkitService(object):
    """Toolkit class to control the workflow.

    This class provides methods to connect to HFSS and create geometries.

    Parameters
    ----------
    None

    Attributes
    ----------
    aedtapp : obj
        AEDT application object.
    multiplier : float
        Multiplier value.
    comps : list
        List of components.

    """

    def __init__(self, service_generic):
        self.aedtapp = None
        self.multiplier = 1.0
        self.comps = []
        self.service_generic = service_generic

    @pyaedt_function_handler()
    def connect_hfss(self):
        """Connect to HFSS.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> service_generic = ServiceGeneric()
        >>> service_generic.launch_aedt()
        >>> toolkit = ToolkitService(service_generic)
        >>> toolkit.connect_hfss()

        """
        if isinstance(self.service_generic.aedt_runner.desktop, type(Desktop())):
            if not self.aedtapp:
                if not self.service_generic.aedt_runner.desktop.design_list():  # pragma: no cover
                    # If no design exist then create a new HFSS design
                    self.aedtapp = Hfss(
                        specified_version=self.service_generic.aedt_runner.desktop.aedt_version_id,
                        aedt_process_id=self.service_generic.aedt_runner.desktop.aedt_process_id,
                        new_desktop_session=False,
                    )
                else:
                    oproject = self.service_generic.aedt_runner.desktop.odesktop.GetActiveProject()
                    projectname = oproject.GetName()
                    activedesign = oproject.GetActiveDesign().GetName()
                    self.aedtapp = self.service_generic.aedt_runner.desktop[
                        [projectname, activedesign]
                    ]
            return True
        return False

    @pyaedt_function_handler()
    def create_geometry(self):
        """Create geometry.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> service_generic = ServiceGeneric()
        >>> service_generic.launch_aedt()
        >>> toolkit = ToolkitService(service_generic)
        >>> toolkit.create_geometry()
        """
        multiplier = self.service_generic.get_properties()["multiplier"]
        geometry = self.service_generic.get_properties()["geometry"]
        self.multiplier = multiplier
        if geometry == "Box":
            comp = self.draw_box()
        elif geometry == "Sphere":
            comp = self.draw_sphere()
        else:
            return False
        self.comps.append(comp)
        return True

    @pyaedt_function_handler()
    def draw_box(self):
        """Draw a box.

        Returns
        -------
        :class:`pyaedt.modeler.object3d.Object3d`
            3D object.
        """
        props = self._comp_props()
        pos_x = props[0][0]
        pos_y = props[0][1]
        pos_z = props[0][2]

        box = self.aedtapp.modeler.create_box(
            position=[pos_x, pos_y, pos_z],
            dimensions_list=[1 * self.multiplier, 1 * self.multiplier, 1 * self.multiplier],
        )

        box.color = (props[1][0], props[1][1], props[1][2])
        return box

    @pyaedt_function_handler()
    def draw_sphere(self):
        """Draw a sphere.

        Returns
        -------
        :class:`pyaedt.modeler.object3d.Object3d`
            3D object.

        """

        props = self._comp_props()
        pos_x = props[0][0]
        pos_y = props[0][1]
        pos_z = props[0][2]

        sp = self.aedtapp.modeler.create_sphere(
            position=[pos_x, pos_y, pos_z],
            radius=1 * self.multiplier,
        )

        sp.color = (props[1][0], props[1][1], props[1][2])
        return sp

    @pyaedt_function_handler()
    def _comp_props(self):
        """Return a random position and color.

        Returns
        -------
        tuple[list, list]

        """
        pos = [np.random.random() * 20, np.random.random() * 20, np.random.random() * 20]
        r = str(np.random.randint(0, 255))
        g = str(np.random.randint(0, 255))
        b = str(np.random.randint(0, 255))

        return pos, [r, g, b]
