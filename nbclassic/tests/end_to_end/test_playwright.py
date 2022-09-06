"""Proof of concept for playwright testing, uses a reimplementation of test_execute_code"""


from playwright.sync_api import Page, expect

# TODO: Remove
# from selenium.webdriver.common.keys import Keys
# from .utils import shift, cmdtrl


def test_execute_code(notebook):
    # browser = notebook.browser

    # def clear_outputs():
    #     return notebook.evaluate(
    #         "Jupyter.notebook.clear_all_output();")
    page = notebook.page
    page.pause()
    page.reload()
    title = page.title()
    # notebook_a_tag = page.locator('a[href=\"http://localhost:8888/a@b/notebooks/Untitled.ipynb\"]')
    notebook_a_tag = page.locator('#notebook_list > div:nth-child(4) > div > a')
    new_page = notebook_a_tag.click()
    page.goto('http://localhost:8888/a@b/notebooks/Untitled.ipynb')

    # Execute cell with Javascript API
    notebook.edit_cell(index=0, content='a=10; print(a)')
    notebook.evaluate("Jupyter.notebook.get_cell(0).execute();")
    outputs = notebook.wait_for_cell_output(0)
    assert outputs.inner_text().strip() == '10'

    # # Execute cell with Shift-Enter
    # notebook.edit_cell(index=0, content='a=11; print(a)')
    # clear_outputs()
    # shift(notebook.browser, Keys.ENTER)
    # outputs = notebook.wait_for_cell_output(0)
    # assert outputs[0].text == '11'
    # notebook.delete_cell(index=1)
    #
    # # Execute cell with Ctrl-Enter
    # notebook.edit_cell(index=0, content='a=12; print(a)')
    # clear_outputs()
    # cmdtrl(notebook.browser, Keys.ENTER)
    # outputs = notebook.wait_for_cell_output(0)
    # assert outputs[0].text == '12'
    #
    # # Execute cell with toolbar button
    # notebook.edit_cell(index=0, content='a=13; print(a)')
    # clear_outputs()
    # notebook.browser.find_element_by_css_selector(
    #     "button[data-jupyter-action='jupyter-notebook:run-cell-and-select-next']").click()
    # outputs = notebook.wait_for_cell_output(0)
    # assert outputs[0].text == '13'
    #
    # # Set up two cells to test stopping on error
    # notebook.edit_cell(index=0, content='raise IOError')
    # notebook.edit_cell(index=1, content='a=14; print(a)')
    #
    # # Default behaviour: stop on error
    # clear_outputs()
    # browser.execute_script("""
    #     var cell0 = Jupyter.notebook.get_cell(0);
    #     var cell1 = Jupyter.notebook.get_cell(1);
    #     cell0.execute();
    #     cell1.execute();
    # """)
    # outputs = notebook.wait_for_cell_output(0)
    # assert notebook.get_cell_output(1) == []
    #
    # # Execute a cell with stop_on_error=false
    # clear_outputs()
    # browser.execute_script("""
    #         var cell0 = Jupyter.notebook.get_cell(0);
    #         var cell1 = Jupyter.notebook.get_cell(1);
    #         cell0.execute(false);
    #         cell1.execute();
    #     """)
    # outputs = notebook.wait_for_cell_output(1)
    # assert outputs[0].text == '14'