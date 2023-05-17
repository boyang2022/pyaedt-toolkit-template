Backend toolkit service
=======================
This section list the available toolkit methods in the backend:

.. currentmodule:: ansys.aedt.toolkits.template.backend.service

.. autosummary::
   :toctree: _autosummary

   ToolkitService

The API must be used using PyAEDT as in the following example:

.. code:: python

    # Import backend
    from ansys.aedt.toolkits.template.backend.service import ToolkitService

    # Initialize generic service
    service = ToolkitService()

    # Get the default properties loaded from json file
    properties = service.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2022.2"}
    service.set_properties(new_properties)
    properties = service.get_properties()

    # Launch AEDT
    msg = service.launch_aedt()

    # Create geometry
    msg = service.create_geometry()

    # Desktop is released here
    service.release_desktop()
