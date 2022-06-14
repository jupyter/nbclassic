"""Shim the notebook module for the classic extensions.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import sys

def shim_notebook_6():
    """Define in sys.module the needed notebook packages that should be fullfilled by
    their corresponding and backwards-compatible jupyter-server packages.

    TODO Can we lazy load these loading.
    
    Note: We could a custom module loader to achieve similar functionality. The 
    logic thar conditional loading seems to be more complicated than simply
    listing by hand the needed subpackages but could avoid latency on server start.
    
    https://docs.python.org/3/library/importlib.html#importlib.abc.Loader

    These are the notebook packages we need to shim:

    auth
    base
    bundler <- no, already available in nbclassic
    edit <- no, already available in nbclassic
    files
    gateway
    i18n <- no, already available in nbclassic
    kernelspecs
    nbconvert
    notebook <- no, already available in nbclassic
    prometheus
    services
    static <- no, already available in nbclassic
    templates <- no, already available in nbclassic
    terminal <- no, already available in nbclassic
    tests <- no, already available in nbclassic
    tree <- no, already available in nbclassic
    view
    __init__.py <- no, already available in nbclassic
    __main__.py <- no, already available in nbclassic
    _sysinfo.py <- no, already available in nbclassic
    _tz.py
    _version.py <- no, already available in nbclassic
    config_manager.py <- no, already available in nbclassic
    extensions.py <- no, already available in nbclassic
    jstest.py <- no, already available in nbclassic
    log.py
    nbextensions.py <- no, already available in nbclassic
    notebookapp.py <- no, already available in nbclassic
    serverextensions.py <- no, already available in nbclassic
    traittypes.py <- no, already available in nbclassic
    transutils.py <- no, already available in nbclassic
    utils.py

    """
    sys.modules["notebook.auth"] = __import__("jupyter_server.auth")
    sys.modules["notebook.base"] = __import__("jupyter_server.base")
    sys.modules["notebook.files"] = __import__("jupyter_server.files")
    sys.modules["notebook.gateway"] = __import__("jupyter_server.gateway")
    sys.modules["notebook.kernelspecs"] = __import__("jupyter_server.kernelspecs")
    sys.modules["notebook.nbconvert"] = __import__("jupyter_server.nbconvert")
    sys.modules["notebook.prometheus"] = __import__("jupyter_server.prometheus")
    sys.modules["notebook.services"] = __import__("jupyter_server.services")
    sys.modules["notebook.view"] = __import__("jupyter_server.view")
    sys.modules["notebook._tz"] = __import__("jupyter_server._tz")
    sys.modules["notebook.log"] = __import__("jupyter_server.log")
    sys.modules["notebook.utils"] = __import__("jupyter_server.utils")


def shim_notebook_7_and_above():
    """For now, notebook v7 should be shimmed for now the same way 
    as notebook v6. This distinction could be useful for later 
    notebook >=7 evolutions.

    TODO Discuss and remove if not needed.
    """
    shim_notebook_6()
