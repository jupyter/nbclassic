"""Test readonly notebook saved and renamed"""


from .utils import EDITOR_PAGE


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
    notebook_frontend.wait_for_selector(".input", page=EDITOR_PAGE)

    # Set a name for comparison later
    set_notebook_name(notebook_frontend, name="nb1.ipynb")
    assert get_notebook_name(notebook_frontend) == "nb1.ipynb"

    # Wait for Save As modal, save
    save_as(notebook_frontend)

    # Wait for modal to pop up
    notebook_frontend.wait_for_selector('//input[@data-testid="save-as"]', page=EDITOR_PAGE)

    # TODO: Add a function for locator assertions to FrontendElement
    locator_element = notebook_frontend.locate_and_focus('//input[@data-testid="save-as"]', page=EDITOR_PAGE)
    locator_element.wait_for('visible')

    notebook_frontend.insert_text('new_notebook.ipynb', page=EDITOR_PAGE)

    notebook_frontend.try_click_selector('//html//body//div[8]//div//div//div[3]//button[2]', page=EDITOR_PAGE)

    locator_element.wait_for('hidden')

    notebook_frontend.locate('#notebook_name', page=EDITOR_PAGE)

    # Test that the name changed
    assert get_notebook_name(notebook_frontend) == "new_notebook.ipynb"

    # Test that address bar was updated
    assert "new_notebook.ipynb" in notebook_frontend.get_page_url(page=EDITOR_PAGE)
