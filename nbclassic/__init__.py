import os
import sys
from ._version import __version__ 

# Packagers: modify this line if you store the notebook static files elsewhere
DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "static")

# Notebook shim to ensure notebook extensions do not break.
try:
    from notebook._version import __version__ as notebook_version
    if notebook_version < "7":
        from .shim_notebook import shim_notebook_6
        shim_notebook_6()
    else:
        from .shim_notebook import shim_notebook_7_and_above
        shim_notebook_7_and_above()
except:
    # Notebook is not available on the platform.
    # We just shim the complete notebook module.
    import jupyter_server
    sys.modules["notebook"] = jupyter_server

# Include both nbclassic/ and nbclassic/templates/.  This makes it
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
