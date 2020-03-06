from .notebookapp import NotebookApp


def _jupyter_server_extension_paths():
    return [{
        'mod': 'nbclassic.notebookapp',
        'app': NotebookApp
    }]