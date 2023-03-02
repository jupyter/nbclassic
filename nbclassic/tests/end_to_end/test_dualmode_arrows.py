"""Tests arrow keys on both command and edit mode"""


from .utils import EDITOR_PAGE


JS_HAS_SELECTED = "(element) => { return element.classList.contains('selected'); }"


def test_dualmode_arrows(notebook_frontend):

    # Tests in command mode.
    # Setting up the cells to test the keys to move up.
    notebook_frontend.to_command_mode()
    count = 1
    for _ in range(3):
        count += 1
        notebook_frontend.press("b", page=EDITOR_PAGE)
        notebook_frontend.wait_for_condition(
            lambda: len(notebook_frontend.cells) == count
        )

    def await_cell_edit_ready_state(cell_index):
        notebook_frontend.wait_for_condition(
            lambda: notebook_frontend.cells[cell_index].evaluate(JS_HAS_SELECTED) is True
        )
        print('/IMG/cell has selected/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
        if not notebook_frontend.cells[cell_index].locate('.CodeMirror-focused').is_visible():
            print('/IMG/Before enter pressed/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
            notebook_frontend.press("Enter", page=EDITOR_PAGE)
            print('/IMG/keypressed enter/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
            notebook_frontend.wait_for_condition(
                lambda: notebook_frontend.cells[cell_index].locate('.CodeMirror-focused').is_visible()
            )
            print('/IMG/codemirror is focused/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
        return True

    # CodeMirror-focused

    # Use both "k" and up arrow keys to moving up and enter a value.
    # Once located on the top cell, use the up arrow keys to prove the top cell is still selected.
    # ............................................
    notebook_frontend.press("k", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(2),
        timeout=330,
        period=5
    )
    notebook_frontend.press("2", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_cell_contents(index=2) == '2'
    )
    notebook_frontend.to_command_mode()
    # ..................................................
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(1),
        timeout=330,
        period=5
    )
    notebook_frontend.press("1", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_cell_contents(index=1) == '1'
    )
    notebook_frontend.to_command_mode()
    # ............................................
    print('/IMG/before_arrow_to_top/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    notebook_frontend.press("k", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    print('/IMG/before_readycheck/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(0),
        timeout=330,
        period=5
    )
    print('/IMG/after_readycheck/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    notebook_frontend.press("0", page=EDITOR_PAGE)
    print('/IMG/after_press0/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_cell_contents(index=0) == '0'
    )
    print('/IMG/cell content is 0/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    notebook_frontend.to_command_mode()
    assert notebook_frontend.get_cells_contents() == ["0", "1", "2", ""]

    # Use the "k" key on the top cell as well
    notebook_frontend.press("k", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(0),
        timeout=330,
        period=5
    )
    notebook_frontend.type(" edit #1", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", ""]

    # Setting up the cells to test the keys to move down
    [notebook_frontend.press("j", page=EDITOR_PAGE) for i in range(3)]
    [notebook_frontend.press("a", page=EDITOR_PAGE) for i in range(2)]
    notebook_frontend.press("k", page=EDITOR_PAGE)

    # Use both "j" key and down arrow keys to moving down and enter a value.
    # Once located on the bottom cell, use the down arrow key to prove the bottom cell is still selected.
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(3),
        timeout=330,
        period=5
    )
    notebook_frontend.press("3", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    notebook_frontend.press("j", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(4),
        timeout=330,
        period=5
    )
    notebook_frontend.press("4", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    notebook_frontend.press("j", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(5),
        timeout=330,
        period=5
    )
    notebook_frontend.press("5", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5"]

    # Use the "j" key on the top cell as well
    notebook_frontend.press("j", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(5),
        timeout=330,
        period=5
    )
    notebook_frontend.type(" edit #1", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5 edit #1"]

    # On the bottom cell, use both left and right arrow keys to prove the bottom cell is still selected.
    notebook_frontend.press("ArrowLeft", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(6),
        timeout=330,
        period=5
    )
    notebook_frontend.type(", #2", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5 edit #1, #2"]
    notebook_frontend.press("ArrowRight", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: await_cell_edit_ready_state(6),
        timeout=330,
        period=5
    )
    notebook_frontend.type(" and #3", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5 edit #1, #2 and #3"]

    # Tests in edit mode.
    # First, erase the previous content and then setup the cells to test the keys to move up.
    [notebook_frontend.locate(".fa-cut.fa", page=EDITOR_PAGE).click() for i in range(6)]
    [notebook_frontend.press("b", page=EDITOR_PAGE) for i in range(2)]
    notebook_frontend.press("a", page=EDITOR_PAGE)
    notebook_frontend.press("Enter", page=EDITOR_PAGE)

    # Use the up arrow key to move down and enter a value.
    # We will use the left arrow key to move one char to the left since moving up on last character only moves selector to the first one.
    # Once located on the top cell, use the up arrow key to prove the top cell is still selected.
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.press("1", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowLeft", page=EDITOR_PAGE)
    [notebook_frontend.press("ArrowUp", page=EDITOR_PAGE) for i in range(2)]
    notebook_frontend.press("0", page=EDITOR_PAGE)

    # Use the down arrow key to move down and enter a value.
    # We will use the right arrow key to move one char to the right since moving down puts selector to the last character.
    # Once located on the bottom cell, use the down arrow key to prove the bottom cell is still selected.
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowRight", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.press("2", page=EDITOR_PAGE)
    [notebook_frontend.press("ArrowDown", page=EDITOR_PAGE) for i in range(2)]
    notebook_frontend.press("3", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    assert notebook_frontend.get_cells_contents() == ["0", "1", "2", "3"]
