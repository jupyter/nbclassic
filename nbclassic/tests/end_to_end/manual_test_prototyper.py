"""Test basic cell execution methods, related shortcuts, and error modes"""


from .utils import TREE_PAGE, EDITOR_PAGE


def test_do_something(notebook_frontend):
    # Do something with the notebook_frontend here
    notebook_frontend.add_cell()
    notebook_frontend.add_cell()
    assert len(notebook_frontend.cells) == 3

    notebook_frontend.delete_all_cells()
    assert len(notebook_frontend.cells) == 1

    notebook_frontend.editor_page.pause()
    cell_texts = ['aa = 1', 'bb = 2', 'cc = 3']
    a, b, c = cell_texts
    notebook_frontend.populate(cell_texts)
    assert notebook_frontend.get_cells_contents() == [a, b, c]
    notebook_frontend._pause()
