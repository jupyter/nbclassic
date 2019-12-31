import pytest
from nbclassic.notebookapp import NotebookApp

pytest_plugins = "pytest_jupyter_server"


@pytest.fixture
def notebookapp(serverapp):
    app = NotebookApp()
    app.initialize(serverapp)
    return app