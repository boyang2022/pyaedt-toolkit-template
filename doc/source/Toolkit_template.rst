======================
New toolkit guidelines
======================

This repository is a template for any new PyAEDT toolkit. It standardizes PyAEDT toolkits implementation.

The **PyAEDT Toolkit Template** is a working toolkit able to connect to an existing AEDT session, open an existing
AEDT project or initialize a new AEDT session, which should be the basic capability of any toolkit.
In addition, it creates boxes and spheres in random positions as an example of AEDT control.

There are common parts which should not be modified, and others which could be different depending on
the new toolkit implementation. In the following sections, it is defined best practices to implement your own toolkit.

Create a new repository in GitHub
---------------------------------

The first step is to create a new repository, it could be Private, Internal, or Public,
you could start making it Private.

You could create this repository inside the `PyAnsys organization <https://github.com/pyansys>`_.
If you're an employee of `Ansys Inc. <https://github.com/pyansys>`_,
you can join the organization by visiting
`Join PyAnsys. <https://myapps.microsoft.com/signin/
8f67c59b-83ac-4318-ae96-f0588382ddc0?tenantId=34c6ce67-15b8-4eff-80e9-52da8be89706>`_.

If you're external to Ansys but want to contribute to adding a new toolkit,
please open an issue on `PyAEDT <https://aedt.docs.pyansys.com/version/stable//>`_.

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

#. Mirror-push to the new repository:

    .. code:: bash

      cd OLD-REPOSITORY.git
      git push --mirror https://github.com/pyansys/pyaedt-toolkit-new_toolkit_name.git

#. Remove the temporary local repository you created earlier:

    .. code:: bash

      cd ..
      rm -rf OLD-REPOSITORY.git

#. Create a clone of the new repository:

    .. code:: bash

      cd New-REPOSITORY-Path
      git clone https://github.com/pyansys/pyaedt-toolkit-new_toolkit_name.git


Modify general settings
-----------------------

There are some parts in the repository which are specific for each different toolkit and must be modified manually.

#. Modify the folder name src/ansys/aedt/toolkits/toolkit_name/template to
src/ansys/aedt/toolkits/toolkit_name/new_toolkit_name

#. Modify .github/workflows/ci_cd.yml file, from line 16 to 20, with the specific toolkit name.

#. Modify .github/workflows/ci_cd.yml file, line 89, with the specific toolkit name.

#. Modify .pre-commit-config.yml file, line 3, with the corresponding UI path.

#. Modify pyproject.toml file, line 7 and 9, with the corresponding toolkit name and description.

#. Modify pyproject.toml file, line 57, with the corresponding toolkit name.

#. Modify pyproject.toml file, from line 60 to 61, with the corresponding toolkit name.

Install default dependencies
----------------------------

You can install in the virtual environment the basic packages to run a PyAEDT toolkit, like pyaedt or pyside6.

.. code:: bash

  pip install .
  pip install .[tests]
  pip install .[doc]
  pip install pre-commit
  pre-commit install


Create backend
--------------

The backend part controls all related to AEDT. It should contain code which could be launched without a user interface.

On this repository you have a simple example, you will find in other toolkits more examples of how to develop a backend.
It should be created in src/ansys/aedt/toolkits/new_toolkit_name/backend.

Create unit test
----------------

If the repository has a backend, you should create unit test for each different method, this will increase
the maintainability of your code. File tests/test_00_template.py contains unittest for the backend methods.

Depending on the complexity of the unit tests, it could need AEDT or not to run the tests.

If AEDT needs to be run, the GitHub actions will try to connect to a runner called *pyaedt-toolkits*, please submit an issue
on the `PyAEDT Issues <https://github.com/pyansys/PyAEDT/issues>`_ page and PyAnsys organizers will give access to this toolkit.

If the unit tests do not need AEDT, then you could modify the .github/workflows/ci_cd.yml and remove line 63.

Create user interface
---------------------

If you installed the default dependencies, you installed pyside6, which allows to create user interfaces.
Please visit its website for more information.
General guidelines for user interface implementation are:

#. Open the designer.

    .. code:: bash

       pyside6-designer

#. Open the ui template in src/ansys/aedt/toolkits/new_toolkit_name/ui/toolkit.ui.

#. Modify it and save it.

#. Create a new python script, which contains these modifications.

    .. code:: bash

        pyside6-uic src\ansys\aedt\toolkits\new_toolkit_name\ui\toolkit.ui -o src\ansys\aedt\toolkits\new_toolkit_name\ui\ui_main.py

#. Create your script to control this user interface.


Create documentation
--------------------

The documentation is created automatically using Sphinx. You need to define the structure in the doc/source/index.rst

#. Modify doc/source/conf.py lines 16, 20, 31, 36, 46 and 57 with the toolkit name.

#. Remove the file doc/source/Toolkit_template.py and line 12 from doc/source/index.rst.

#. Modify README.rst, this is the first page when you open the documentation.

#. Modify all rst files in doc/source

#. You can build the documentation locally:

    .. code:: bash

        cd doc\source
        create_documentation.bat

#. To publish the documentation online, you will need to submit an issue on the `PyAEDT Issues <https://github.com/pyansys/PyAEDT/issues>`_ page and PyAnsys organizers will add the URL to the Ansys servers.


Add toolkit in PyAEDT
---------------------

Create an issue on the `PyAEDT Issues <https://github.com/pyansys/PyAEDT/issues>`_ page,
and PyAEDT contributors will add it to the method *add_custom_toolkit*.