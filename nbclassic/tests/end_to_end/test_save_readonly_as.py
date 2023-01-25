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
    print('[Test] Begin test_save_readonly_as body')
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
    # notebook_frontend.wait_for_selector('//input[@data-testid="save-as"]', page=EDITOR_PAGE)
    notebook_frontend.wait_for_selector(".modal-footer", page=EDITOR_PAGE)
    dialog_element = notebook_frontend.locate(".modal-footer", page=EDITOR_PAGE)
    dialog_element.focus()

    # TODO: Add a function for locator assertions to FrontendElement
    # locator_element = notebook_frontend.locate_and_focus('//input[@data-testid="save-as"]', page=EDITOR_PAGE)
    # locator_element.wait_for('visible')

    # modal_footer = notebook_frontend.locate('.modal-footer', page=EDITOR_PAGE)
    # modal_footer.wait_for('visible')

    # notebook_frontend.insert_text('new_notebook.ipynb', page=EDITOR_PAGE)
    print('[Test] Focus the notebook name input field, then click and modify its .value')
    name_input_element = notebook_frontend.wait_for_selector('.modal-body .form-control', page=EDITOR_PAGE)
    name_input_element.focus()
    name_input_element.click()
    name_input_element.evaluate(f'(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}')
    notebook_frontend.wait_for_condition(
        lambda: name_input_element.evaluate(f'(elem) => {{ return elem.value; }}') == 'new_notebook.ipynb',
        timeout=120,
        period=.25
    )

    print('[Test] Name input field contents:')
    print('[Test] ' + name_input_element.evaluate(f'(elem) => {{ return elem.value; }}'))

    notebook_frontend._editor_page.pause()
    # save_btn = modal_footer.locate('text=Save')
    # save_btn.wait_for('visible')
    # save_btn.click()
    # notebook_frontend.try_click_selector('//html//body//div[8]//div//div//div[3]//button[2]', page=EDITOR_PAGE)
    print('[Test] Locate and click the save button')
    save_element = dialog_element.locate('text=Save')
    save_element.wait_for('visible')
    save_element.focus()
    save_element.click()

    # Try to ensure the save button is hidden (the prompt went away)
    print('[Test] Check save button visibility to ensure prompt is gone')
    if save_element.is_visible():
        print('[Test] Save button visible, waiting for hidden...')
        try:
            save_element.expect_not_to_be_visible()
        except Exception as err:
            traceback.print_exc()
            print('\n[Test] Failure waiting for save button hidden, see error above')

        if save_element.is_visible():
            try:
                print('[Test] Save button still visible! Likely error...')
                save_message_element = notebook_frontend.locate('.modal-body .save-message', page=EDITOR_PAGE)
                print('[Test] Contents of the save-message element:')
                print('[Test] ' + save_message_element.get_inner_text())
            except Exception as err:
                traceback.print_exc()
                print('\n[Test] Error retrieving save message (see above), continuing...')
    else:
        print('[Test] Save button is hidden, continuing')

    notebook_frontend._editor_page.pause()
    # locator_element.expect_not_to_be_visible()
    notebook_frontend.wait_for_condition(
        lambda: get_notebook_name(notebook_frontend) == "new_notebook.ipynb", timeout=120, period=5
    )

    # notebook_frontend.locate('#notebook_name', page=EDITOR_PAGE)

    # # Test that the name changed
    # assert get_notebook_name(notebook_frontend) == "new_notebook.ipynb"

    # Test that address bar was updated
    assert "new_notebook.ipynb" in notebook_frontend.get_page_url(page=EDITOR_PAGE)
