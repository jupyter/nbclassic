from os import rename
from tkinter import E
from webbrowser import get
from .utils import EDITOR_PAGE, TREE_PAGE
import time


# TODO: TEST TIMESOUT WHEN NOT RUN IN DEBUG MODE: DUE TO wait_for_selector('.cell') CALL IN _open_notebook_editor_page
        # WHEN IN DEBUG MODE, HAVE TO RELOAD THE PAGE FOR THE .cell SELECTOR TO BE PICKED UP
        # determine when to wait for the selector.....
def check_for_rename(nb, selector, page, new_name):
    check_count = 0
    nb_name = nb.locate(selector, page)
    while nb_name != new_name and check_count <= 5:
        nb_name = nb.locate(selector, page)
        check_count += 1
    return nb_name

def save_as(nb):
    JS = '() => Jupyter.notebook.save_notebook_as()'
    return nb.evaluate(JS, page=EDITOR_PAGE)

def get_notebook_name(nb):
    JS = '() => Jupyter.notebook.notebook_name'
    return nb.evaluate(JS, page=EDITOR_PAGE)

def set_notebook_name(nb, name):
    JS = f'() => Jupyter.notebook.rename("{name}")'
    nb.evaluate(JS, page=EDITOR_PAGE)

def test_save_notebook_as(notebook_frontend):
    notebook_frontend.edit_cell(index=0, content='a=10; print(a)')
    notebook_frontend.wait_for_kernel_ready()
    notebook_frontend.editor_page.wait_for_selector(".input")

    # Set a name for comparison later
    set_notebook_name(notebook_frontend, name="nb1.ipynb")
    assert get_notebook_name(notebook_frontend) == "nb1.ipynb"

    # Wait for Save As modal, save
    save_as(notebook_frontend)
    notebook_frontend.editor_page.wait_for_selector('.save-message')

    inp = notebook_frontend.editor_page.wait_for_selector('//input[@data-testid="save-as"]')
    inp.type('new_notebook.ipynb')
    notebook_frontend.try_click_selector('//html//body//div[8]//div//div//div[3]//button[2]', page=EDITOR_PAGE)

    check_for_rename(notebook_frontend, '#notebook_name', page=EDITOR_PAGE, new_name="new_notebook.ipynb")

    # notebook_frontend.editor_page.query_selector('#notebook_name')
    # notebook_frontend.editor_page.query_selector('#notebook_name')
    # notebook_frontend.editor_page.query_selector('#notebook_name')
    # notebook_frontend.editor_page.query_selector('#notebook_name')

    # Test that the name changed
    assert get_notebook_name(notebook_frontend) == "new_notebook.ipynb"

    # Test that address bar was updated (TODO: get the base url)
    print(f"editor_page dir: {dir(notebook_frontend.editor_page)}")
    assert "new_notebook.ipynb" in notebook_frontend.editor_page.url