"""Test save-as functionality"""

import sys
import time
import traceback
from functools import partial

import pytest

from .utils import EDITOR_PAGE, EndToEndTimeout


def save_as(nb):
    JS = '() => Jupyter.notebook.save_notebook_as()'
    return nb.evaluate(JS, page=EDITOR_PAGE)


def get_notebook_name(nb):
    JS = '() => Jupyter.notebook.notebook_name'
    return nb.evaluate(JS, page=EDITOR_PAGE)


def set_notebook_name(nb, name):
    JS = f'() => Jupyter.notebook.rename("{name}")'
    nb.evaluate(JS, page=EDITOR_PAGE)


@pytest.mark.skipif(sys.platform == 'darwin', reason="fails randomly on osx")
def test_save_as_nb(notebook_frontend):
    print('[Test] [test_save_as_notebook]')
    notebook_frontend.wait_for_kernel_ready()
    notebook_frontend.wait_for_selector(".input", page=EDITOR_PAGE)

    # Set a name for comparison later
    print('[Test] Set notebook name')
    set_notebook_name(notebook_frontend, name="nb1.ipynb")
    notebook_frontend.wait_for_condition(
        lambda: get_notebook_name(notebook_frontend) == 'nb1.ipynb',
        timeout=150,
        period=1
    )

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

    fill_attempts = 0

    def attempt_form_fill_and_save(notebook_path):
        # Application behavior here is HIGHLY variable, we use this for repeated attempts
        # ....................
        # This may be a retry, check if the application state reflects a successful save operation
        nonlocal fill_attempts
        if fill_attempts and get_notebook_name(notebook_frontend) == notebook_path.split("/")[-1]:
            print('[Test]   Success from previous save attempt!')
            return True
        fill_attempts += 1
        print(f'[Test] Attempt form fill and save #{fill_attempts}')

        # Make sure the save prompt is visible
        if not name_input_element.is_visible():
            save_as(notebook_frontend)
            name_input_element.wait_for('visible')

        # Set the notebook name field in the save dialog
        print('[Test] Fill the input field')
        name_input_element.evaluate('(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}')
        notebook_frontend.wait_for_condition(
            lambda: name_input_element.evaluate(
                '(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}') == 'new_notebook.ipynb',
            timeout=120,
            period=.25
        )
        # Show the input field value
        print('[Test] Name input field contents:')
        field_value = name_input_element.evaluate('(elem) => {{ return elem.value; }}')
        print('[Test]   ' + field_value)
        if field_value != 'new_notebook.ipynb':
            return False

        print('[Test] Locate and click the save button')
        save_element = dialog_element.locate('text=Save')
        save_element.wait_for('visible')
        save_element.focus()
        save_element.click()
        time.sleep(3)
        print('[Test] Save button clicked')

        # If the notebook already exists from previous attempts or other tests,
        # just overwrite it
        if notebook_frontend.locate('text=Overwrite', page=EDITOR_PAGE).is_visible():
            overwrite_element = notebook_frontend.locate('text=Overwrite', page=EDITOR_PAGE)
            overwrite_element.focus()
            overwrite_element.click()
            time.sleep(3)

        save_element.wait_for('detached')
        print('[Test] Save element detached')

        # Application lag may cause the save dialog to linger,
        # if it's visible wait for it to disappear before proceeding
        if save_element.is_visible():
            print('[Test] Save element still visible after save, wait for hidden')
            try:
                save_element.expect_not_to_be_visible(timeout=120)
            except EndToEndTimeout as err:
                traceback.print_exc()
                print('[Test]   Save button failed to hide...')

        # Check if the save operation succeeded (by checking notebook name change)
        notebook_frontend.wait_for_condition(
            lambda: get_notebook_name(notebook_frontend) == "new_notebook.ipynb", timeout=120, period=5
        )
        print(f'[Test] Notebook name: {get_notebook_name(notebook_frontend)}')
        print('[Test] Notebook name was changed!')
        return True

    # Retry until timeout (wait_for_condition retries upon func exception)
    notebook_frontend.wait_for_condition(
        partial(attempt_form_fill_and_save, "new_notebook.ipynb"),
        timeout=120,
        period=1,
    )

    print('[Test] Check notebook name in URL')
    notebook_frontend.wait_for_condition(
        lambda: get_notebook_name(notebook_frontend) in notebook_frontend.get_page_url(page=EDITOR_PAGE),
        timeout=120,
        period=5
    )

    print('[Test] Begin attempts to fill the save dialog input and save the notebook with a new directory')
    fill_attempts=0

    def attempt_form_fill_w_dir_and_save(notebook_path):
        # Application behavior here is HIGHLY variable, we use this for repeated attempts
        # ....................
        # This may be a retry, check if the application state reflects a successful save operation
        nonlocal fill_attempts
        if fill_attempts and get_notebook_name(notebook_frontend) == notebook_path.split("/")[-1]:
            print('[Test] Success from previous save attempt!')
            return True
        fill_attempts += 1
        print(f'[Test] Attempt form fill with directory and save #{fill_attempts}')

        # Make sure the save prompt is visible
        if not name_input_element.is_visible():
            save_as(notebook_frontend)
            name_input_element.wait_for('visible')

        # Set the notebook name field in the save dialog
        print('[Test] Fill the input field')
        name_input_element.evaluate(f'(elem) => {{ elem.value = "{notebook_path}"; return elem.value; }}')
        notebook_frontend.wait_for_condition(
            lambda: name_input_element.evaluate(
                f'(elem) => {{ elem.value = "{notebook_path}"; return elem.value; }}') == notebook_path,
            timeout=120,
            period=.25
        )
        # Show the input field value
        print('[Test] Name input field contents:')
        field_value = name_input_element.evaluate('(elem) => {{ return elem.value; }}')
        print('[Test]   ' + field_value)
        if field_value != notebook_path:
            return False

        print('[Test] Locate and click the save button')
        save_element = dialog_element.locate('text=Save')
        save_element.wait_for('visible')
        save_element.focus()
        save_element.click()
        time.sleep(3)
        print('[Test] Save button clicked')

        # If the notebook path contains a directory, click the create button
        if "/" in notebook_path:
            print('[Test] Locate and click the create button')
            create_element = dialog_element.locate('text=Create')
            create_element.wait_for('visible')
            create_element.focus()
            create_element.click()
            time.sleep(3)

        # If the notebook already exists from previous attempts or other tests,
        # just overwrite it
        if notebook_frontend.locate('text=Overwrite', page=EDITOR_PAGE).is_visible():
            overwrite_element = notebook_frontend.locate('text=Overwrite', page=EDITOR_PAGE)
            overwrite_element.focus()
            overwrite_element.click()
            time.sleep(3)

        # Application lag may cause the save dialog to linger,
        # if it's visible wait for it to disappear before proceeding
        if save_element.is_visible():
            print('[Test] Save element still visible after save, wait for hidden')
            try:
                save_element.expect_not_to_be_visible(timeout=120)
            except EndToEndTimeout as err:
                traceback.print_exc()
                print('[Test]   Save button failed to hide...')

        # Check if the save operation succeeded (by checking notebook name change)
        notebook_frontend.wait_for_condition(
            lambda: get_notebook_name(notebook_frontend) == notebook_path.split('/')[-1], timeout=120, period=5
        )
        print(f'[Test] Notebook name: {get_notebook_name(notebook_frontend)}')
        print('[Test] Notebook name was changed!')
        return True

    for notebook_path in ["new_notebook.ipynb", "new_folder/another_new_notebook.ipynb"]:
        print(f'[Test] Begin attempts to fill the save dialog input with {notebook_path} and save the notebook')
        fill_attempts = 0
        check_func = partial(attempt_form_fill_w_dir_and_save, notebook_path)
        notebook_frontend.wait_for_condition(check_func, timeout=900, period=1)

        print('[Test] Check notebook name in URL')
        try:
            notebook_frontend.wait_for_condition(
                lambda: notebook_path.split("/")[-1] in notebook_frontend.get_page_url(page=EDITOR_PAGE),
                timeout=120,
                period=5
            )
        except:
            print(notebook_frontend.get_page_url(page=EDITOR_PAGE))
