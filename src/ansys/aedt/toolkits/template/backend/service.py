import numpy as np

from ansys.aedt.toolkits.template.backend.common.logger_handler import logger
from ansys.aedt.toolkits.template.backend.common.service_generic import ServiceGeneric
from ansys.aedt.toolkits.template.backend.common.service_generic import thread


class ToolkitService(ServiceGeneric):
    """Toolkit class to control the toolkit workflow.

    This class provides methods to connect to HFSS and create geometries.

    Examples
    --------
    >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
    >>> service = ToolkitService()
    >>> msg1 = service.launch_aedt()
    >>> msg2 = service.connect_aedt()
    >>> msg3 = service.create_geometry()
    >>> service.release_desktop()
    """

    def __init__(self):
        ServiceGeneric.__init__(self)
        self.multiplier = 1.0
        self.comps = []

    @thread.launch_thread
    def create_geometry(self):
        """Create a box or a sphere in HFSS.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> service.connect_aedt()
        >>> service.create_geometry()
        """
        if self.connect_aedtapp("Hfss"):
            properties = self.get_properties()
            multiplier = properties["multiplier"]
            geometry = properties["geometry"]
            self.multiplier = multiplier
            comp = None
            if geometry == "Box":
                comp = self.draw_box()
            elif geometry == "Sphere":
                comp = self.draw_sphere()
            if comp:
                self.comps.append(comp)
            self.release_desktop()
            return True
        else:  # pragma: no cover
            return False

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
        logger.debug("Box {} created".format(box.name))
        return box

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
        logger.debug("Sphere {} created".format(sp.name))
        return sp

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
