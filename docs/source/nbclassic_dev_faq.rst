.. _nbclassic_dev_faq:

Developer FAQ
=============

1. Where should I submit my issue?

The Jupyter Notebook v6.4.x will only be taking security fixes, you can follow
these guidelines to `report a vulnerability`_.

For Notebook v6.5.x, as it is intended to be end of life and will receive only
bug and security fixes, issues of this type in the frontend should be reported in
the `jupyter/nbclassic`_ repository, bug and security issues for the server can be
submitted in the `jupyter/notebook`_ repository. 

Generally, user interface issues dealing with the nbclassic package can be
submitted to the `jupyter/nbclassic`_ repository, while server issues can be
reported to the `jupyter_server/jupyter_server`_ repository.

Notebook v7.x issues would require closer consideration as they could be
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