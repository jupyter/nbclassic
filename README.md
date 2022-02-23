# Jupyter Notebook as a Jupyter Server Extension

![Testing nbclassic](https://github.com/jupyterlab/nbclassic/workflows/Testing%20nbclassic/badge.svg)


NBClassic runs the [Jupyter Notebook](https://github.com/jupyter/notebook) frontend on the Jupyter Server backend.

This project prepares for a future where JupyterLab and other frontends switch to [Jupyter Server](https://github.com/jupyter/jupyter_server/) for their Python Web application backend. Using this package, users can launch Jupyter Notebook, JupyterLab and other frontends side-by-side on top of the new Python server backend.

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
