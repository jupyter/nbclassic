# Jupyter Notebook as a Jupyter Server Extension

![Testing nbclassic](https://github.com/jupyterlab/nbclassic/workflows/Testing%20nbclassic/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/nbclassic/badge/?version=latest)](https://nbclassic.readthedocs.io/en/latest/?badge=latest)

NBClassic is the classic Jupyter Notebook application (with the classic
Javascript interface) running on Jupyter Server.

This project provides compatibility with the old notebook interface and
support during an intermediate transition period to Notebook 7, for users
with extensions and other customizations that cannot yet be upgraded
to the new version of Notebook.

In the future, Jupyter frontends like NBClassic and JupyterLab will coexist
side-by-side on top of a [Jupyter Server] backend. This package makes that
possible: You can install this package beside an existing JupyterLab or
Jupyter Notebook 7 environment, and get the best of both worlds:

- The newest features from the latest applications
- Compatibility for older classic extensions and tools that are important
  to existing workflows, but that cannot yet be converted to the new versions

## Basic Usage

Install from PyPI:
```
> pip install nbclassic
```
This will automatically enable the extension in Jupyter Server.

Launch directly:
```
> jupyter nbclassic
```

Alternatively, you can run Jupyter Server and visiting the `/tree` endpoint:
```
> jupyter server
```

[Jupyter Server]: https://github.com/jupyter/jupyter_server/
