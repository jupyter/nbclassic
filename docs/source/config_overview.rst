======================
Configuration Overview
======================

As NbClassic is a Jupyter Server Extension that is intended as an intermediary project while users
migrate from Notebook 6 to Notebook 7, this document makes references to configuration
files carried over from the classic Jupyter Notebook which will be executed when running
nbclassic. For more general documentation regarding the Jupyter Server that NbClassic
uses please visit the `Jupyter Server documentation <https://jupyter-server.readthedocs.io/en/latest/index.html>`_.

Beyond the default configuration settings, you can configure a rich array of
options to suit your workflow. Here are areas that are commonly configured
when using Jupyter NbClassic:

    - :ref:`Jupyter's common configuration system <configure_common>`
    - :ref:`NbClassic server <configure_nbserver>`
    - :ref:`NbClassic front-end client <configure_nbclient>`
    - :ref:`Notebook extensions <configure_nbextensions>`

Let's look at highlights of each area.

.. _configure_common:

Jupyter's Common Configuration system
-------------------------------------
Jupyter applications, from the Notebook to JupyterHub to nbgrader, share a
common configuration system. The process for creating a configuration file
and editing settings is similar for all the Jupyter applications.

    - `Jupyter’s Common Configuration Approach <https://jupyter.readthedocs.io/en/latest/use/config.html>`_
    - `Common Directories and File Locations <https://jupyter.readthedocs.io/en/latest/use/jupyter-directories.html>`_
    - `Language kernels <https://jupyter.readthedocs.io/en/latest/projects/kernels.html>`_
    - `traitlets <https://traitlets.readthedocs.io/en/latest/config.html#module-traitlets.config>`_
      provide a low-level architecture for configuration.

.. _configure_nbserver:

NbClassic Server
----------------
The NbClassic server runs the language kernel and communicates with the
front-end NbClassic client (i.e. the familiar notebook interface).

  - Configuring the NbClassic server

      To create a ``jupyter_notebook_config.py`` file in the ``.jupyter``
      directory, with all the defaults commented out, use the following
      command::

            $ jupyter nbclassic --generate-config

      :ref:`Command line arguments for configuration <config>` settings are documented in the configuration file and the user documentation.

  - Review the section: :ref:`Running a Notebook server <working_remotely>`
  - Related: `Configuring a language kernel <https://ipython.readthedocs.io/en/latest/install/kernel_install.html>`_
    to run in the Notebook server enables your server to run other languages, like R or Julia.

.. _configure_nbclient:

NbClassic front-end client
--------------------------

.. toctree::
   :maxdepth: 2

   frontend_config

.. _configure_nbextensions:

Notebook extensions
-------------------
- `Distributing Jupyter Extensions as Python Packages <https://jupyter-notebook.readthedocs.io/en/v6.5.4/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html#Distributing-Jupyter-Extensions-as-Python-Packages>`_
- `Extending the Notebook <https://jupyter-notebook.readthedocs.io/en/stable/extending/index.html>`_


:ref:`Security in Jupyter notebooks:  <notebook_security>` Since security
policies vary from organization to organization, we encourage you to
consult with your security team on settings that would be best for your use
cases. Our documentation offers some responsible security practices, and we
recommend becoming familiar with the practices.
