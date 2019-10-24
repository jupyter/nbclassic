# nbclassic: Jupyter Notebook Server Extension

**A package that provides a simple transition away from Jupyter Notebook to Jupyter Server.**

This library allows you to install both [jupyter/notebook](http://localhost:8888/tree) and a Jupyter Notebook Server Extension side-by-side (and any other Jupyter Server Frontend).

This helps projects like JupyterLab and nteract_on_jupyter transition from jupyter/notebook to jupyter/jupyter_server for the core Jupyter Tornado Server.

## Install

Install from PyPI:
```
pip install nbclassic
```

Launch with Jupyter Server:
```
jupyter server
```
and go to: http://localhost:8888/tree?token=...
