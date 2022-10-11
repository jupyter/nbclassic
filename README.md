# Jupyter Notebook as a Jupyter Server Extension

![Testing nbclassic](https://github.com/jupyterlab/nbclassic/workflows/Testing%20nbclassic/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/nbclassic/badge/?version=latest)](https://nbclassic.readthedocs.io/en/latest/?badge=latest)

NBClassic runs the [Jupyter NbClassic](https://github.com/jupyter/nbclassic) frontend on the Jupyter Server backend.

This project prepares for a future where JupyterLab and other frontends switch to [Jupyter Server](https://github.com/jupyter/jupyter_server/) for their Python Web application backend. Using this package, users can launch Jupyter NbClassic, JupyterLab and other frontends side-by-side on top of the new Python server backend.

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
