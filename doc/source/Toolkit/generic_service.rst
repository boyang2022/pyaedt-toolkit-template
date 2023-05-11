Backend generic service
=======================
This section list the available generic methods in the backend, these methods are the same for all toolkits:

.. currentmodule:: ansys.aedt.toolkits.template.backend.service_generic

.. autosummary::
   :toctree: _autosummary

   set_properties
   get_properties
   aedt_connected
   installed_aedt_version
   aedt_sessions
   launch_aedt
   release_desktop
   open_project


The API must be used using PyAEDT as in the following example:

.. code:: python

    # Import backend
    import ansys.aedt.toolkits.template.backend.service_generic as service_generic

    # Get the default properties loaded from json file
    properties = service_generic.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2022.2"}
    service_generic.set_properties(new_properties)
    properties = service_generic.get_properties()

    # Launch AEDT
    msg = service_generic.launch_aedt()

    # Desktop is released here
    service_generic.release_desktop()


