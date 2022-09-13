"""Proof of concept for playwright testing, uses a reimplementation of test_execute_code"""


from .utils import TREE_PAGE, EDITOR_PAGE


def test_execute_code(notebook_frontend):
    # Execute cell with Javascript API
    notebook_frontend.edit_cell(index=0, content='a=10; print(a)')
    notebook_frontend.evaluate("Jupyter.notebook.get_cell(0).execute();", page=EDITOR_PAGE)
    outputs = notebook_frontend.wait_for_cell_output(0)
    assert outputs.inner_text().strip() == '10'  # TODO fix/encapsulate inner_text

    # Execute cell with Shift-Enter
    notebook_frontend.edit_cell(index=0, content='a=11; print(a)')
    notebook_frontend.clear_all_output()
    notebook_frontend.press("Shift+Enter", EDITOR_PAGE)
    outputs = notebook_frontend.wait_for_cell_output(0)
    assert outputs.inner_text().strip() == '11'
    notebook_frontend.delete_cell(1)  # Shift+Enter adds a cell

    # TODO fix for platform-independent execute logic (mac uses meta+enter)
    # Execute cell with Ctrl-Enter (or equivalent)
    notebook_frontend.edit_cell(index=0, content='a=12; print(a)')
    notebook_frontend.clear_all_output()
    notebook_frontend.press("Control+Enter", EDITOR_PAGE)
    outputs = notebook_frontend.wait_for_cell_output(0)
    assert outputs.inner_text().strip() == '12'

    # Execute cell with toolbar button
    notebook_frontend.edit_cell(index=0, content='a=13; print(a)')
    notebook_frontend.clear_all_output()
    notebook_frontend.click_toolbar_execute_btn()
    outputs = notebook_frontend.wait_for_cell_output(0)
    assert outputs.inner_text().strip() == '13'
    notebook_frontend.delete_cell(1)  # Toolbar execute button adds a cell

    # Set up two cells to test stopping on error
    notebook_frontend.type('a', EDITOR_PAGE)
    notebook_frontend.edit_cell(index=0, content='raise IOError')
    notebook_frontend.edit_cell(index=1, content='a=14; print(a)')

    # Default behaviour: stop on error
    notebook_frontend.clear_all_output()
    notebook_frontend.evaluate("""
        var cell0 = Jupyter.notebook.get_cell(0);
        var cell1 = Jupyter.notebook.get_cell(1);
        cell0.execute();
        cell1.execute();
    """, page=EDITOR_PAGE)
    outputs = notebook_frontend.wait_for_cell_output(0)
    assert notebook_frontend.get_cell_output(1) is None

    # Execute a cell with stop_on_error=false
    notebook_frontend.clear_all_output()
    notebook_frontend.evaluate("""
            var cell0 = Jupyter.notebook.get_cell(0);
            var cell1 = Jupyter.notebook.get_cell(1);
            cell0.execute(false);
            cell1.execute();
        """, page=EDITOR_PAGE)
    outputs = notebook_frontend.wait_for_cell_output(1)
    assert outputs.inner_text().strip() == '14'
