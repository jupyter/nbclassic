:html_theme.sidebar_secondary.remove:

=================
Jupyter NbClassic
=================
.. toctree::
   :maxdepth: 2
   
Introduction
------------

The nbclassic package is the implementation of the classic Jupyter
Notebook 6 as a Jupyter Server extension. As proposed in the accepted
`Jupyter Enhancement Proposal #79`_ the development of this package
is due to plans being carried out to create a Notebook 7, that is based on
the modern JupyterLab code-base. 

While Notebook 7 provides a user experience equivalent to that of the
classic Notebook 6, the technology stack used is incompatible with
that which many Jupyter Notebook users have developed their Jupyter
Notebook extensions with. Users may find themselves in need of a
way to continue using the Jupyter Notebook 6 tech-stack as they
transition to using the Jupyter Notebook 7. The NbClassic package
intends to address that need.

You can read more about the migration impacts and coexistence of NbClassic and Notebook package on 
the `NbClassic and Notebook migration plan <https://jupyter-notebook.readthedocs.io/en/latest/migrate_to_notebook7.html>`_ page.

.. _Jupyter Enhancement Proposal #79: https://jupyter.org/enhancement-proposals/79-notebook-v7/notebook-v7.html

.. _NbClassicUsage:

NbClassic Usage
---------------

Installation
~~~~~~~~~~~~

Installing from PyPI:
``pip install nbclassic``
This will automatically enable the extension in Jupyter Server.

Launch directly:
``jupyter nbclassic``

Alternatively, you can run Jupyter Server and visit the `/tree` endpoint:
``jupyter server``

Configuration
~~~~~~~~~~~~~

To create a ``jupyter_nbclassic_config.py`` file in the ``.jupyter`` directory you can use the following command::
    
    $ jupyter nbclassic --generate-config

Options
~~~~~~~

You can view a list of the available options by typing::

    $ jupyter nbclassic --help
    

NbClassic Development
---------------------

`Nbclassic <https://github.com/jupyter/nbclassic>`_ is the package that holds the UI components of
the classic Jupyter Notebook 6 and serves this UI through the server
endpoints provided by Jupyter Server.

*Jupyter Server Extensions*
- `Authoring a basic server extension <https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html>`_

**The jupyter/notebook Repository**: The original `jupyter/notebook`_ GitHub 
repository now holds the codebase for the new Jupyter Notebook (version 7).

.. _jupyter/notebook: https://github.com/jupyter/notebook


NbClassic Timeline
------------------
As proposed in the `JEP #79`_, the nbclassic
package will continue to be supported with critical security fixes
in the transition period as users move to using the more modern 
Jupyter Notebook 7.

**Porting Notebook 6 Extensions**: Work being done in parallel. 
ou can find a helpful list of classical Notebook extensions and corresponding Jupyterlab extensions
if available at the `Jupyterlab-contrib website <https://jupyterlab-contrib.github.io/migrate_from_classical.html>`_.

.. _JEP #79: https://jupyter.org/enhancement-proposals/79-notebook-v7/notebook-v7.html

Known issues
------------

Bellow are some known bugs and issues with the NbClassic project. These are items that may be of particular interest to users
migrating from notebook to nbclassic.

1. `#140 Error using jupyter_nbextensions_configurator with nbclassic <https://github.com/jupyter/nbclassic/issues/140>`_ is a 
known issue with partial fix `Support nbclassic while updating the static path <https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator/pull/141>`_ 
pending to be merged into the `Jupyter-contrib/jupyter_nbextensions_configurator <https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator>`_ repository.

    Once a release with this fix is available, users will be able to activate the extension with the following commands::

    $ pip install 'jupyter_nbextensions_configurator @ git+https://github.com/datalayer-externals/jupyter-notebook-configurator.git@fix/nbclassic#egg=jupyter_nbextensions_configurator'
    $ jupyter nbclassic-extension install --sys-prefix --py jupyter_nbextensions_configurator --overwrite
    $ jupyter nbclassic-extension enable --sys-prefix --py jupyter_nbextensions_configurator
    $ jupyter nbclassic-serverextension enable --sys-prefix --py jupyter_nbextensions_configurator
