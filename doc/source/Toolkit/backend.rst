Backend Template
================
This section list the available bowtie antennas:

.. currentmodule:: ansys.aedt.toolkits.template.backend.template_script

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   TemplateBackend

The API must be used using PyAEDT as in the following example:

.. code:: python

    # Launch AEDT
    from pyaedt import Hfss

    aedtapp = Hfss(
        specified_version="2023.1",
        non_graphical=False,
        new_desktop_session=True,
        close_on_exit=True,
    )
    # Import backend
    from ansys.aedt.toolkits.template.backend.template_script import TemplateBackend

    # Backend object
    template = TemplateBackend(aedtapp)

    # Create a box in a random position
    b = template.draw_box()

    # Desktop is released here
    aedtapp.release_desktop()


