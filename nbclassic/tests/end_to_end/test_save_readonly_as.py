"""Test readonly notebook saved and renamed"""


import traceback

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
    print('[Test] [test_save_readonly_as]')
    notebook_frontend.edit_cell(index=0, content='a=10; print(a)')
    notebook_frontend.wait_for_kernel_ready()
    notebook_frontend.wait_for_selector(".input", page=EDITOR_PAGE)

    # Set a name for comparison later
    print('[Test] Set notebook name')
    set_notebook_name(notebook_frontend, name="nb1.ipynb")
    assert get_notebook_name(notebook_frontend) == "nb1.ipynb"

    # Wait for Save As modal, save
    print('[Test] Save')
    save_as(notebook_frontend)

    # # Wait for modal to pop up
    print('[Test] Waiting for modal popup')
    notebook_frontend.wait_for_selector(".modal-footer", page=EDITOR_PAGE)
    dialog_element = notebook_frontend.locate(".modal-footer", page=EDITOR_PAGE)
    dialog_element.focus()

    print('[Test] Focus the notebook name input field, then click and modify its .value')
    notebook_frontend.wait_for_selector('.modal-body .form-control', page=EDITOR_PAGE)
    name_input_element = notebook_frontend.locate('.modal-body .form-control', page=EDITOR_PAGE)
    name_input_element.focus()
    name_input_element.click()

    # Begin attempts to fill the save dialog input and save the notebook
    fill_attempts = 1

    def attempt_form_fill_and_save():
        # This process is SUPER flaky, we use this for repeated attempts
        nonlocal fill_attempts
        print(f'[Test] Attempt form fill and save #{fill_attempts}')
        if fill_attempts >= 1 and get_notebook_name(notebook_frontend) == "new_notebook.ipynb":
            print('[Test]   Success from previous save attempt!')
            return True
        fill_attempts += 1

        # Set the notebook name field in the save dialog
        print('[Test] Fill the input field')
        name_input_element.evaluate(f'(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}')
        notebook_frontend.wait_for_condition(
            lambda: name_input_element.evaluate(
                f'(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}') == 'new_notebook.ipynb',
            timeout=120,
            period=.25
        )
        # Show the input field value
        print('[Test] Name input field contents:')
        field_value = name_input_element.evaluate(f'(elem) => {{ return elem.value; }}')
        print('[Test]   ' + field_value)
        if field_value != 'new_notebook.ipynb':
            return False

        print('[Test] Locate and click the save button')
        save_element = dialog_element.locate('text=Save')
        save_element.wait_for('visible')
        save_element.focus()
        save_element.click()

        if save_element.is_visible():
            print('[Test] Save element still visible after save, wait for hidden')
            try:
                save_element.expect_not_to_be_visible(timeout=120)
            except Exception as err:
                traceback.print_exc()
                print('[Test]   Save button failed to hide...')

        notebook_frontend.wait_for_condition(
            lambda: get_notebook_name(notebook_frontend) == "new_notebook.ipynb", timeout=120, period=5
        )
        print(f'[Test] Notebook name: {get_notebook_name(notebook_frontend)}')
        print('[Test] Notebook name was changed!')
        return True

    # Retry until timeout, this process is *very* flaky
    notebook_frontend.wait_for_condition(attempt_form_fill_and_save, timeout=900, period=1)

    # Test that address bar was updated
    print('[Test] Test address bar')
    assert "new_notebook.ipynb" in notebook_frontend.get_page_url(page=EDITOR_PAGE)
