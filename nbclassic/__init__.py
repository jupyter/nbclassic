from .notebookapp import NotebookApp

EXTENSION_NAME = "notebook_shim"

def _jupyter_server_extension_paths():
    return [{"module": EXTENSION_NAME}]

load_jupyter_server_extension = NotebookApp.load_jupyter_server_extension 