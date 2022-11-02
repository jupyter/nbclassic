"""Basic tests for the notebook handlers.
"""

import pytest


@pytest.fixture
def notebooks(jp_create_notebook):
    nbpaths = (
        'notebook1.ipynb',
        'nbclassic_test_notebooks/notebook2.ipynb',
        'nbclassic_test_notebooks/level2/notebook3.ipynb'
    )
    for nb in nbpaths:
        jp_create_notebook(nb)
    return nbpaths


config = pytest.mark.parametrize(
    "jp_server_config",
    [
        {
            "ServerApp": {
                "contents_manager_class": "jupyter_server.services.contents.largefilemanager.LargeFileManager",
                "jpserver_extensions": {
                    "nbclassic": True,
                    "notebook_shim": True
                }
            },
        },
        {
            "ServerApp": {
                "contents_manager_class": "jupyter_server.services.contents.largefilemanager.AsyncLargeFileManager",
                "jpserver_extensions": {
                    "nbclassic": True,
                    "notebook_shim": True
                }
            },
        }
    ],
)

@config
async def test_tree_handler(notebooks, jp_fetch):
    r = await jp_fetch('tree', 'nbclassic_test_notebooks')
    assert r.code == 200

    # Check that the tree template is loaded
    html = r.body.decode()
    assert "Files" in html
    assert "Running" in html
    assert "Clusters" in html


@config
async def test_notebook_handler(notebooks, jp_fetch):
    for nbpath in notebooks:
        r = await jp_fetch('notebooks', nbpath)
        assert r.code == 200
        # Check that the notebook template is loaded
        html = r.body.decode()
        assert "Menu" in html
        assert "Kernel" in html
        assert nbpath in html


@config
async def test_edit_handler(notebooks, jp_fetch):
    r = await jp_fetch('edit', 'notebook1.ipynb')
    assert r.code == 200
    html = r.body.decode()
    assert "<title>notebook1.ipynb" in html


async def test_terminal_handler(jp_fetch):
        r = await jp_fetch('terminals', "1")
        assert r.code == 200
        # Check that the terminals template is loaded
        html = r.body.decode()
        assert "terminal-app" in html
