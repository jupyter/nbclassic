The Development of NbClassic
============================

Here you will find information about some especially noteworthy updates made in NbClassic, issues that have been reported 
and common questions.


Noteworthy Updates in NbClassic 
--------------------------------

- Entrypoints in NbClassic
    - In NbClassic entrypoints have been renamed (`Rename duplicate entrypoints #138`_) to:

        - ``jupyter-nbclassic-extension``
        - ``jupyter nbclassic-serverextension``
        - ``jupyter-nbclassic-bundlerextension``

    - The decision to rename these entrypoints came about after some deliberation and consideration for user experience. When considering the confusion that having a more implicit handling of the entrypoints might pose, the concensus was that renaming the entrypoints would allow for more observability and it would help highlight some of the changes that are happening in the Jupyter ecosystem.  

.. _`Rename duplicate entrypoints #138`: https://github.com/jupyter/nbclassic/pull/138


- Providing backwards compatibility with the  `jupyter_notebook_config.py` file
    - With the goal of allowing NbClassic to be installed along with Notebook 7, the release of NbClassic 0.4 included changing the project name from `notebook` to `nbclassic`. In changing the 'name' attribute to be `nbclassic`, the traitlet behavior changed and resulted in the configuration file which was previously named `jupyter_notebook_config`, to be named `jupyter_nbclassic_config`. However, this was updated to manually set the file name to `jupyter_notebook_config`. With this, the configuration file is picked up whether Notebook or NbClassic are installed. 

- Endpoints in NbClassic
    - NbClassic handlers have been updated to account for Notebook 7 being installed (`Handlers under nbclassic if notebook 7 is found`_). If so, the resources from nbclassic will be served under the ``/nbclassic/`` URL subpath, so as to not interfere  with those resources being served by Jupyter Notebook.
    - Redirecting from ``/tree`` to ``/nbclassic/tree`` if both Notebook 7 and NbClassic are installed (`PR #166`_).

.. _`Handlers under nbclassic if notebook 7 is found`: https://github.com/jupyter/nbclassic/pull/141
.. _`PR #166`: https://github.com/jupyter/nbclassic/pull/166



NbClassic Developer FAQ
-----------------------

1. Where should I submit my issue?

    The Jupyter Notebook 6.4.x will only be taking security fixes, you can follow
    these guidelines to `report a vulnerability`_.

    For Notebook 6.5.x, as it is intended to be end of life and will receive only
    bug and security fixes, issues of this type in the frontend should be reported in
    the `jupyter/nbclassic`_ repository, bug and security issues for the server can be
    submitted in the `jupyter/notebook`_ repository. 

    Generally, user interface issues dealing with the nbclassic package can be
    submitted to the `jupyter/nbclassic`_ repository, while server issues can be
    reported to the `jupyter_server/jupyter_server`_ repository.

    Notebook 7.x issues would require closer consideration as they could be
    reported in the `jupyter/notebook`_, `jupyterlab/jupyterlab`_, or
    `jupyter_server/jupyter_server`_ repositories depending on the issue.

    .. _`report a vulnerability`: https://github.com/jupyter/security/blob/main/docs/vulnerability-handling.md#reporting-vulnerabilities
    .. _`jupyter/nbclassic`: https://github.com/jupyter/nbclassic
    .. _`jupyter/notebook`: https://github.com/jupyter/notebook
    .. _`jupyter_server/jupyter_server`: https://github.com/jupyter-server/jupyter_server
    .. _`jupyterlab/jupyterlab`: https://github.com/jupyterlab/jupyterlab

    The Jupyter Community appreciates your efforts in making sure your issue is submitted to the correct project.
    There are many projects within the Jupyter ecosystem which can mean some issues are best suited for repositories
    different than those in which they may have been opened. In the case that the issue belongs in a different
    repository, we can use the `MeeseeksDev bot`_ to move the issue to the appropriate repository so long as the
    target repository is included in the `allowed organization list`_ in the MeeseeksDev codebase. You can see a
    list of the Github links to Jupyter organizations, and the different Jupyter projects under each, in the
    `Jupyter Community`_ page.

    .. _`MeeseeksDev bot`: https://github.com/MeeseeksBox/MeeseeksDev#meeseeksdev-migrate-to-target-orgrepo
    .. _`allowed organization list`: https://github.com/MeeseeksBox/MeeseeksDev/blob/master/meeseeksdev/__init__.py#L26
    .. _`Jupyter Community`: https://jupyter.org/community


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
