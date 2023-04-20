==========================
New toolkit implementation
==========================

This repository is a template for any new PyAEDT toolkit. It standardizes the way of PyAEDT toolkits implementation, it
will make these toolkits easier to maintain, improve and understand.
The **PyAEDT Toolkit Template** is a working toolkit able to connect to an existing AEDT session, open an existing
AEDT project or initialize a new AEDT session. There are common parts which should not be modified, and others
which will be different depending on the new toolkit implementation.
In the following sections, we will define best practices to implement your own toolkit.

Create a new repository in GitHub
---------------------------------

The first step is to create a new repository, it could be Private at the beginning and then make it Internal or Public.
You could create this repository inside the `PyAnsys organization <https://github.com/pyansys>`_.
If you're an employee of `Ansys Inc. <https://github.com/pyansys>`_,
you can join the organization by visiting
`Join PyAnsys. <https://myapps.microsoft.com/signin/
8f67c59b-83ac-4318-ae96-f0588382ddc0?tenantId=34c6ce67-15b8-4eff-80e9-52da8be89706>`_.

If you're external to Ansys but want to contribute to adding a new toolkit,
please open an issue on `PyAEDT <https://aedt.docs.pyansys.com/version/stable//>`_ and we'll consider adding
the new repository.

The naming convention for PyAEDT toolkits is **pyaedt-toolkit-new_toolkit_name**.

.. image:: ./_static/new_repo.png
  :width: 800
  :alt: New PyAnsys repository

Duplicate the template repository
---------------------------------

Before you can push the template repository to your new repository, you must create the new repository on GitHub.com.

#. Open Git Bash.

#. Create a bare clone of the repository:

   .. code:: bash

      git clone --bare https://github.com/pyansys/pyaedt-toolkit-template.git

#. Mirror-push to the new repository (in this case called "new_toolkit_name"):

    .. code:: bash

      cd OLD-REPOSITORY.git
      git push --mirror https://github.com/pyansys/pyaedt-toolkit-new_toolkit_name.git

#. Remove the temporary local repository you created earlier:

    .. code:: bash

      cd ..
      rm -rf OLD-REPOSITORY.git

.. image:: ./Resources/toolkit_in_AEDT.png
  :width: 800
  :alt: PyAEDT toolkit installed


Modify general settings
-----------------------

There are some parts in the repository which are specific for each different toolkit and we need to modify manually.
In this section we will modify all of them.

Create backend
--------------

Create unittest
---------------

Create user interface
---------------------

Create documentation
--------------------

Add toolkit in PyAEDT
---------------------
