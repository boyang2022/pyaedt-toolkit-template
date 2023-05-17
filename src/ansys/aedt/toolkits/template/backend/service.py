import numpy as np
from pyaedt import Desktop
from pyaedt import Hfss

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
    >>> msg2 = service.create_geometry()
    >>> service.release_desktop()
    """

    def __init__(self):
        ServiceGeneric.__init__(self)
        self.aedtapp = None
        self.multiplier = 1.0
        self.comps = []

    def connect_hfss(self):
        """Connect to HFSS design. If HFSS design exists, it takes the active project and design,
         if not, it creates a new HFSS design.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> service.connect_hfss()

        """
        if isinstance(self.aedt_runner.desktop, type(Desktop())):
            if not self.aedtapp:
                if not self.aedt_runner.desktop.design_list():
                    properties = self.get_properties()
                    # If no design exist then create a new HFSS design
                    self.aedtapp = Hfss(
                        specified_version=self.aedt_runner.desktop.aedt_version_id,
                        aedt_process_id=self.aedt_runner.desktop.aedt_process_id,
                        non_graphical=properties["non_graphical"],
                        new_desktop_session=False,
                    )
                else:  # pragma: no cover
                    oproject = self.aedt_runner.desktop.odesktop.GetActiveProject()
                    projectname = oproject.GetName()
                    activedesign = oproject.GetActiveDesign().GetName()
                    self.aedtapp = self.aedt_runner.desktop[[projectname, activedesign]]
            return True
        return False

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
        >>> service.create_geometry()
        """
        hfss_connect = self.connect_hfss()
        if hfss_connect:
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
            return True
        else:  # pragma: no cover
            return False

    @thread.launch_thread
    def save_project(self):
        """Save project.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> from ansys.aedt.toolkits.template.backend.service import ToolkitService
        >>> service = ToolkitService()
        >>> service.launch_aedt()
        >>> service.save_project()
        """
        hfss_connect = self.connect_hfss()
        if hfss_connect:
            properties = self.get_properties()
            new_project_name = properties["new_project_name"]
            self.aedt_runner.desktop.save_project(project_path=new_project_name)
            return True
        else:
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
