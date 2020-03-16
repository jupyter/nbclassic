from .notebookapp import NotebookApp


def _jupyter_server_extension_paths():
    return [{
        'module': 'nbclassic.notebookapp',
        'app': NotebookApp
    }]