"""Fixtures for pytest/playwright end_to_end tests."""


import os
import json
import sys
import time
from os.path import join as pjoin
from subprocess import Popen
from tempfile import mkstemp
from urllib.parse import urljoin

import pytest
import requests
from testpath.tempdir import TemporaryDirectory

import nbformat
from nbformat.v4 import new_notebook, new_code_cell
from .utils import NotebookFrontend, BROWSER, BROWSER_RAW, TREE_PAGE, SERVER_INFO


def _wait_for_server(proc, info_file_path):
    """Wait 30 seconds for the notebook server to start"""
    for i in range(300):
        if proc.poll() is not None:
            raise RuntimeError("Notebook server failed to start")
        if os.path.exists(info_file_path):
            try:
                with open(info_file_path) as f:
                    return json.load(f)
            except ValueError:
                # If the server is halfway through writing the file, we may
                # get invalid JSON; it should be ready next iteration.
                pass
        time.sleep(0.1)
    raise RuntimeError("Didn't find %s in 30 seconds", info_file_path)


@pytest.fixture(scope='function')
def notebook_server():
    info = {}
    with TemporaryDirectory() as td:
        nbdir = info['nbdir'] = pjoin(td, 'notebooks')
        os.makedirs(pjoin(nbdir, 'sub ∂ir1', 'sub ∂ir 1a'))
        os.makedirs(pjoin(nbdir, 'sub ∂ir2', 'sub ∂ir 1b'))

        info['extra_env'] = {
            'JUPYTER_CONFIG_DIR': pjoin(td, 'jupyter_config'),
            'JUPYTER_RUNTIME_DIR': pjoin(td, 'jupyter_runtime'),
            'IPYTHONDIR': pjoin(td, 'ipython'),
        }
        env = os.environ.copy()
        env.update(info['extra_env'])

        command = [sys.executable, '-m', 'nbclassic',
                   '--no-browser',
                   '--notebook-dir', nbdir,
                   # run with a base URL that would be escaped,
                   # to test that we don't double-escape URLs
                   '--ServerApp.base_url=/a@b/',
                   ]
        print("command=", command)
        proc = info['popen'] = Popen(command, cwd=nbdir, env=env)
        info_file_path = pjoin(td, 'jupyter_runtime',
                               f'jpserver-{proc.pid:d}.json')
        info.update(_wait_for_server(proc, info_file_path))

        print("Notebook server info:", info)
        yield info

    # Shut the server down
    requests.post(urljoin(info['url'], 'api/shutdown'),
                  headers={'Authorization': 'token '+info['token']})


@pytest.fixture(scope='function')
def playwright_browser(playwright):
    # if os.environ.get('SAUCE_USERNAME'):   # TODO: Fix this
    #     driver = make_sauce_driver()
    if os.environ.get('JUPYTER_TEST_BROWSER') == 'chrome':
        browser = playwright.chromium.launch()
    else:
        browser = playwright.firefox.launch()
    # browser_context = browser.new_context()

    yield browser

    # Teardown
    browser.close()


@pytest.fixture(scope='function')
def authenticated_browser_data(playwright_browser, notebook_server):
    browser_raw = playwright_browser
    playwright_browser = browser_raw.new_context()
    playwright_browser.jupyter_server_info = notebook_server
    tree_page = playwright_browser.new_page()
    tree_page.goto("{url}?token={token}".format(**notebook_server))

    # TODO: fix this mess, BROWSER_RAW naming etc.
    auth_browser_data = {
        BROWSER: playwright_browser,
        TREE_PAGE: tree_page,
        SERVER_INFO: notebook_server,
        BROWSER_RAW: browser_raw,
    }

    return auth_browser_data


@pytest.fixture(scope='function')
def notebook_frontend(authenticated_browser_data):
    # tree_wh = authenticated_browser.current_window_handle
    yield NotebookFrontend.new_notebook_frontend(authenticated_browser_data)
    # authenticated_browser.switch_to.window(tree_wh)


@pytest.fixture(scope='function')
def prefill_notebook(playwright_browser, notebook_server):
    browser_raw = playwright_browser
    playwright_browser = browser_raw.new_context()
    # playwright_browser is the browser_context,
    # notebook_server is the server with directories

    # the return of function inner takes in a dictionary of strings to populate cells
    def inner(cells):
        cells = [new_code_cell(c) if isinstance(c, str) else c
                 for c in cells]
        # new_notebook is an nbformat function that is imported so that it can create a
        # notebook that is formatted as it needs to be 
        nb = new_notebook(cells=cells)

        # Create temporary file directory and store it's reference as well as the path
        fd, path = mkstemp(dir=notebook_server['nbdir'], suffix='.ipynb')

        # Open the file and write the format onto the file
        with open(fd, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

        # Grab the name of the file
        fname = os.path.basename(path)

        # Add the notebook server as a property of the playwright browser with the name jupyter_server_info
        playwright_browser.jupyter_server_info = notebook_server
        # Open a new page in the browser and refer to it as the tree page
        tree_page = playwright_browser.new_page()

        # Navigate that page to the base URL page AKA the tree page
        tree_page.goto("{url}?token={token}".format(**notebook_server))

        auth_browser_data = {
            BROWSER: playwright_browser,
            TREE_PAGE: tree_page,
            SERVER_INFO: notebook_server,
            BROWSER_RAW: browser_raw
        }

        return NotebookFrontend.new_notebook_frontend(auth_browser_data, existing_file_name=fname)

    # Return the function that will take in the dict of code strings
    return inner
