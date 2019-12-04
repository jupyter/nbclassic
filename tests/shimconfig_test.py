"""Test the shimming of the configs.
"""

import os.path
from nbclassic.shimconfig import shim_configs

test_conf_dir = os.path.join(os.getcwd(), 'tests', 'confs')
os.chdir(test_conf_dir)

def test_none():
    """Test None parameters support.
    """
    merged = shim_configs(
        notebook_config_name = None, 
        server_config_name = None, 
        extension_config_name = None, 
        argv = []
        )
    assert merged.NotebookApp != None
    assert merged.ServerApp != None
    assert merged.MyExt != None

def test_merge():
    """Test NotebookApp are copied to ServerApp.
    """

    merged = shim_configs(
        notebook_config_name = 'jupyter_notebook', 
        server_config_name = 'jupyter_nbclassic', 
        extension_config_name = 'jupyter_my_ext', 
        argv = []
        )

    assert merged.NotebookApp.port == 8889
    assert merged.NotebookApp.allow_credentials == False
    assert merged.NotebookApp.password_required == True

    assert merged.ServerApp.port == 8889
    assert merged.ServerApp.allow_credentials == False
    assert merged.ServerApp.password_required == True

    assert merged.MyExt.hello == 'My extension'

def test_merge_cli_order():
    """Test NotebookApp are copied to ServerApp 
    and CLI flags are processed.
    """

    merged = shim_configs(
        notebook_config_name = 'jupyter_notebook', 
        server_config_name = 'jupyter_nbclassic', 
        extension_config_name = 'jupyter_my_ext', 
        argv = [
            '--NotebookApp.port=1111', 
            ]
        )

    assert merged.NotebookApp.port == 1111
    assert merged.NotebookApp.allow_credentials == True
    assert merged.NotebookApp.password_required == True

    assert merged.ServerApp.port == 1111
    assert merged.ServerApp.allow_credentials == True
    assert merged.ServerApp.password_required == True

    assert merged.MyExt.hello == 'My extension'

def test_merge_cli_order():
    """Test NotebookApp are copied to ServerApp 
    and CLI flags are processed in correct order.
    """

    merged = shim_configs(
        notebook_config_name = 'jupyter_notebook', 
        server_config_name = 'jupyter_nbclassic', 
        extension_config_name = 'jupyter_my_ext', 
        argv = [
            '--NotebookApp.port=1111', 
            '--ServerApp.port=2222', 
            '--MyExt.more=True',
            ]
        )

    assert merged.NotebookApp.port == 2222
    assert merged.NotebookApp.allow_credentials == False
    assert merged.NotebookApp.password_required == True

    assert merged.ServerApp.port == 2222
    assert merged.ServerApp.allow_credentials == False
    assert merged.ServerApp.password_required == True

    assert merged.MyExt.hello == 'My extension'
    assert merged.MyExt.more == True
