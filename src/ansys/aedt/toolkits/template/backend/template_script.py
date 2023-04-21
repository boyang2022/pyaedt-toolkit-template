import copy

import numpy as np
from pyaedt.generic.general_methods import pyaedt_function_handler


class TemplateBackend(object):
    """Example of backend class using PyAEDT code. This example creates a box in a random position.

    Your could make a reference [1]_.

    Parameters
    ----------
    color : list, optional
        Box color.

    Returns
    -------
    :class:`pyaedt.modeler.object3d.Object3d`
            3D object.

    Notes
    -----
    .. [1] This is an example of a reference.

    Examples
    --------
    >>> from pyaedt import Hfss
    >>> from ansys.aedt.toolkits.template.backend.template_script import TemplateBackend
    >>> hfss = Hfss()
    >>> template = TemplateBackend(hfss)
    >>> box = template.draw_box()

    """

    _default_input = {
        "dimension_multiplier": 1.0,
    }

    def __init__(self, *args, **kwargs):
        # PyAEDT application object
        self._app = args[0]

        # Copy default values
        self._input_parameters = copy.deepcopy(self._default_input)

        # Modify default values. This is useful when you have more than one parameter to pass.
        for k, v in kwargs.items():
            if k in self._default_input:
                self._input_parameters[k] = v

    @property
    def multiplier(self):
        """Object dimension multiplier.

        Returns
        -------
        list
        """
        return self._input_parameters["multiplier"]

    @multiplier.setter
    def multiplier(self, value):
        self._input_parameters["dimension_multiplier"] = value

    @pyaedt_function_handler()
    def _comp_props(self):
        pos = [np.random.random() * 20, np.random.random() * 20, np.random.random() * 20]
        r = str(np.random.randint(0, 255))
        g = str(np.random.randint(0, 255))
        b = str(np.random.randint(0, 255))

        return pos, [r, g, b]

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

        multiplier = self.multiplier
        box = self._app.modeler.create_box(
            position=[pos_x, pos_y, pos_z],
            dimensions_list=[1 * multiplier, 1 * multiplier, 1 * multiplier],
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

        multiplier = self.multiplier

        sp = self._app.modeler.create_sphere(
            position=[pos_x, pos_y, pos_z],
            radius=1 * multiplier,
        )

        sp.color = (props[1][0], props[1][1], props[1][2])
        return sp
