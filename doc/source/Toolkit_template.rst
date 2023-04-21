==========================
New toolkit implementation
==========================

This repository is a template for any new PyAEDT toolkit. It standardizes PyAEDT toolkits implementation.

The **PyAEDT Toolkit Template** is a working toolkit able to connect to an existing AEDT session, open an existing
AEDT project or initialize a new AEDT session, which should be the basic functionality of any toolkit.
In addition, it creates boxes and spheres in random positions as an example of AEDT control.

There are common parts which should not be modified, and others which will be different depending on
the new toolkit implementation. In the following sections, we will define best practices to implement your own toolkit.

Create a new repository in GitHub
---------------------------------

The first step is to create a new repository, it could be Private, Internal or Public,
you could start making it Private.

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

Duplicate the template in a local repository and then push it in the GitHub repository created in the first step.

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
    .. code:: bash

       pyside6-designer

    .. code:: bash

       pyside6-uic ui\toolkit.ui -o ui\ui_main.py


Create documentation
--------------------

Add toolkit in PyAEDT
---------------------
