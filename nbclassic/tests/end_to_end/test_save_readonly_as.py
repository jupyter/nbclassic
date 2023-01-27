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
    print('/IMG/Before set nb name/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
    set_notebook_name(notebook_frontend, name="nb1.ipynb")
    print('/IMG/After set nb name/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
    assert get_notebook_name(notebook_frontend) == "nb1.ipynb"

    # Wait for Save As modal, save
    print('[Test] Save')
    print('/IMG/Before save/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
    save_as(notebook_frontend)
    print('/IMG/After save/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')

    # # Wait for modal to pop up
    print('[Test] Waiting for modal popup')
    notebook_frontend.wait_for_selector(".modal-footer", page=EDITOR_PAGE)
    print('/IMG/After wait modal popup/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
    dialog_element = notebook_frontend.locate(".modal-footer", page=EDITOR_PAGE)
    dialog_element.focus()

    print('[Test] Focus the notebook name input field, then click and modify its .value')
    name_input_element = notebook_frontend.wait_for_selector('.modal-body .form-control', page=EDITOR_PAGE)
    name_input_element.focus()
    name_input_element.click()
    print('/IMG/Before set field value/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
    notebook_frontend.wait_for_condition(
        lambda: name_input_element.evaluate(f'(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}') == 'new_notebook.ipynb',
        timeout=120,
        period=.25
    )
    # '(elem) => {{ elem.value = "new_notebook.ipynb"; return elem.value; }}'
    print(f"""[Test] VALUE :: {'(elem) => {{ return elem.value; }}'}""")
    print('/IMG/After set field value/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')

    # Show the input field value
    print('[Test] Name input field contents:')
    print('[Test] ' + name_input_element.evaluate(f'(elem) => {{ return elem.value; }}'))

    print('[Test] Locate and click the save button')
    save_element = dialog_element.locate('text=Save')
    save_element.wait_for('visible')
    save_element.focus()
    print('/IMG/Before save btn/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
    save_element.click()
    print('/IMG/After save btn/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')

    # Try to ensure the save button is hidden (the prompt went away)
    print('[Test] Check save button visibility to ensure prompt is gone')
    if save_element.is_visible():
        print('[Test] Save button visible, waiting for hidden...')
        try:
            save_element.expect_not_to_be_visible(timeout=30)
        except Exception as err:
            traceback.print_exc()
            print('[Test] Failure waiting for save button hidden, see error above')

        if save_element.is_visible():
            try:
                print('/IMG/Save btn waiting/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
                print('[Test] Save button still visible! Likely error...')
                save_message_element = notebook_frontend.locate('.modal-body .save-message', page=EDITOR_PAGE)
                print('[Test] Contents of the save-message element:')
                print('[Test] ' + save_message_element.get_inner_text())
            except Exception as err:
                traceback.print_exc()
                print('\n[Test] Error retrieving save message (see above), continuing...')
    else:
        print('[Test] Save button is hidden, continuing')

    print('[Test] Test notebook name change')
    print('/IMG/Before namechange/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')
    # locator_element.expect_not_to_be_visible()
    notebook_frontend.wait_for_condition(
        lambda: get_notebook_name(notebook_frontend) == "new_notebook.ipynb", timeout=120, period=5
    )
    print('/IMG/After namechange/' + notebook_frontend._editor_page.screenshot().hex() + '/IMG/')

    print('[Test] Test address bar')
    # Test that address bar was updated
    assert "new_notebook.ipynb" in notebook_frontend.get_page_url(page=EDITOR_PAGE)
