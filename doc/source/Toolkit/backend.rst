bowtie
======
This section list the available bowtie antennas:

.. currentmodule:: ansys.aedt.toolkits.template.backend.template_script

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   TemplateBackend

The API must be used using PyAEDT as in the following example:

.. code:: python

    from pyaedt import Hfss
    from ansys.aedt.toolkits.antennas.models.bowtie import BowTie

    aedtapp = Hfss(specified_version="2023.1", non_graphical=False)
    # Create antenna
    ohorn = aedtapp.add_from_toolkit(BowTie, draw=True)
    ...
    aedtapp.release_desktop()


