import os
from ._version import __version__ 

# Packagers: modify this line if you store the notebook static files elsewhere
DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "static")

# Packagers: modify the next line if you store the notebook template files
# elsewhere

# Include both notebook/ and notebook/templates/.  This makes it
# possible for users to override a template with a file that inherits from that
# template.
#
# For example, if you want to override a specific block of notebook.html, you
# can create a file called notebook.html that inherits from
# templates/notebook.html, and the latter will resolve correctly to the base
# implementation.
DEFAULT_TEMPLATE_PATH_LIST = [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), "templates"),
]

def _jupyter_server_extension_paths():
    # Locally import to avoid install errors.
    from .notebookapp import NotebookApp

    return [
        {
            'module': 'nbclassic.notebookapp',
            'app': NotebookApp,
            'name': 'jupyter-nbclassic'
        }
    ]
