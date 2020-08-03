
from traitlets import (
    Unicode,
    Bool,
)

from jupyter_server.extension.application import ExtensionApp
from nbclassic import shim


def _jupyter_server_extension_points():
    return [
        {
            "module": "tests.shim.mockextension",
            "app": MockExtensionApp
        }
    ]


class MockExtensionApp(
    shim.NBClassicConfigShimMixin,
    ExtensionApp
):
    """Mock an extension app that previously inherited NotebookApp."""
    name = 'mockextension'

    # ------ Traits found ServerApp, NotebookApp, and MockExtensionApp

    default_url = Unicode(config=True)

    # ------ Traits found Notebook and MockExtensionApp

    enable_mathjax = Bool(config=True)

    # ------ Traits found ServerApp and MockExtensionApp

    allow_origin = Unicode(config=True)
    allow_origin_pat = Unicode(config=True)