"""Test readonly notebook saved and renamed"""


from .utils import EDITOR_PAGE
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def save_as(nb):
    JS = '() => Jupyter.notebook.save_notebook_as()'
    return nb.evaluate(JS, page=EDITOR_PAGE)

def get_notebook_name(nb):
    JS = '() => Jupyter.notebook.notebook_name'
    return nb.evaluate(JS, page=EDITOR_PAGE)

def set_notebook_name(nb, name):
    JS = f'() => Jupyter.notebook.rename("{name}")'
    nb.evaluate(JS, page=EDITOR_PAGE)


def test_save_readonly_as(notebook_frontend):
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
    dialog_element = notebook_frontend.locate_and_focus(".modal-footer", page=EDITOR_PAGE)
    save_element = dialog_element.locate('text=Save')
    save_element.wait_for('visible')
    # locator_element = notebook_frontend.locate_and_focus('//input[@data-testid="save-as"]', page=EDITOR_PAGE)
    # locator_element.wait_for('visible')

    modal_footer = notebook_frontend.locate('.modal-footer', page=EDITOR_PAGE)
    modal_footer.wait_for('visible')

    name_input_element = notebook_frontend.locate('.modal-body', page=EDITOR_PAGE).locate('.form-control')
    name_input_element.click()
    name_input_element.evaluate(f'(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}')
    # notebook_frontend.insert_text('new_notebook.ipynb', page=EDITOR_PAGE)

    save_btn = modal_footer.locate('text=Save')
    save_btn.wait_for('visible')
    save_btn.click()

    notebook_frontend.wait_for_condition(
        lambda: get_notebook_name(notebook_frontend) == "new_notebook.ipynb", timeout=120, period=5
    )

    # notebook_frontend.locate('#notebook_name', page=EDITOR_PAGE)

    # # Test that the name changed
    # assert get_notebook_name(notebook_frontend) == "new_notebook.ipynb"

    # Test that address bar was updated
    assert "new_notebook.ipynb" in notebook_frontend.get_page_url(page=EDITOR_PAGE)
