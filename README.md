# Jupyter Notebook as a Jupyter Server Extension

![Testing nbclassic](https://github.com/Zsailer/nbclassic/workflows/Testing%20nbclassic/badge.svg)


NBClassic runs the [Jupyter Notebook]((github.com/jupyter/notebook)) frontend on the Jupyter Server backend.

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

## Further Details

This project also includes an API for shimming traits that moved from `NotebookApp` in to `ServerApp` in Jupyter Server. This can be used by applications that subclassed `NotebookApp` to leverage the Python server backend of Jupyter Notebooks. Such extensions should *now* switch to `ExtensionApp` API in Jupyter Server and add `NBClassicConfigShimMixin` in their inheritance list to properly handle moved traits.

For example, an application class that previously looked like:
```python
from notebook.notebookapp import NotebookApp

class MyApplication(NotebookApp):
```
should switch to look something like:
```python
from jupyter_server.extension.application import ExtensionApp
from nbclassic.shim import NBClassicConfigShimMixin

class MyApplication(NBClassicConfigShimMixin, ExtensionApp):
```

