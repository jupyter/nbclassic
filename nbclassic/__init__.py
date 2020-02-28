from .notebookapp import NotebookApp

# EXTENSION_NAME = "nbclassic"

# def _jupyter_server_extension_paths():
#     return [{
#         "module": EXTENSION_NAME,
#         "app": NotebookApp
#     }]

_jupyter_server_extension_paths = NotebookApp._jupyter_server_extension_paths
load_jupyter_server_extension = NotebookApp.load_jupyter_server_extension