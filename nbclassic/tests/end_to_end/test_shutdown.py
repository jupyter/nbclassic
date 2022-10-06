"""Tests shutdown of the Kernel."""
from .utils import EDITOR_PAGE

def test_shutdown(prefill_notebook):
    # notebook_frontend.edit_cell(content="print(21)")
    notebook_frontend = prefill_notebook(["print(21)"])
    
    notebook_frontend.try_click_selector('//a[text()="Kernel"]', page=EDITOR_PAGE)
    notebook_frontend.try_click_selector('#shutdown_kernel',  page=EDITOR_PAGE)
    notebook_frontend.try_click_selector('.btn.btn-default.btn-sm.btn-danger', page=EDITOR_PAGE)

    # Wait until all shutdown modal elements disappear before trying to execute the cell
    # notebook_frontend.editor_page.query_selector_all("//div[contains(@class,'modal')]")
    
    notebook_frontend.execute_cell(0)

    assert not notebook_frontend.is_kernel_running()
    assert notebook_frontend.get_cell_output() == None