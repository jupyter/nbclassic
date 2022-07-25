.. _htmlnotebook:

Jupyter NbClassic
====================

Introduction
------------

The nbclassic package is the implementation of the classic Jupyter
Notebook-v6 as a Jupyter Server extension. As proposed in the accepted
`Jupyter Enhancement Proposal #79`_ the development of this package
is due to plans being carried out to create a Notebook-v7, that is based on
the modern JupyterLab code-base. 

While Notebook-v7 provides a user experience equivalent to that of the
classic Notebook-v6, the technology stack used is incompatible with
that which many Jupyter Notebook users have developed their Jupyter
Notebook extensions with. Users may find themselves in need of a
way to continue using the Jupyter Notebook-v6 tech-stack as they
transition to using the Jupyter Notebook-v7. The NbClassic package
intends to address that need.

.. _Jupyter Enhancement Proposal #79: https://jupyter.org/enhancement-proposals/79-notebook-v7/notebook-v7.html


NbClassic Usage
---------------

Using nbclassic, notebook-v7 and jupyterlab

Usign nbclassic and notebook-v6


NbClassic Development
---------------------

Nbclassic is the package that holds the UI components of
the classic Jupyter Notebook-v6 and serves this UI through the server
endpoints provided by Jupyter Server.

**The jupyter/notebook Repository**: The original jupyter/notebook GitHub 
repository now holds the codebase for the new Jupyter Notebook (version 7).


NbClassic Timeline
------------------
As proposed in the `JEP #79`_, the nbclassic
package will continue to be supported with critical security fixes
in the transition period as users move to using the more modern 
Jupyter Notebook-v7.

**Porting Notebook-v6 Extensions**: Work being done in parallel.


.. _JEP #79: https://jupyter.org/enhancement-proposals/79-notebook-v7/notebook-v7.html