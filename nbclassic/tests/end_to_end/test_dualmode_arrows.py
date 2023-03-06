"""Tests arrow keys on both command and edit mode"""
import time

from .utils import EDITOR_PAGE, EndToEndTimeout


INITIAL_CELLS = ['AAA', 'BBB', 'CCC']
JS_HAS_SELECTED = "(element) => { return element.classList.contains('selected'); }"


def test_dualmode_arrows(prefill_notebook):
    # Tests functionality related to up/down arrows and
    # the "j"/"k" shortcuts for up and down, in command
    # mode and in edit mode

    print('[Test] [test_dualmode_arrows] Start!')
    notebook_frontend = prefill_notebook(INITIAL_CELLS)

    # Make sure the top cell is selected
    print('[Test] Ensure top cell is selected')
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.to_command_mode()

    # Move down (shortcut j) to the second cell and check that it's selected
    print('[Test] Move down ("j") to second cell')
    notebook_frontend.press("j", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )

    # Move down to the third cell and check that it's selected
    print('[Test] Move down to third cell')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].evaluate(JS_HAS_SELECTED) is True
    )

    # Move back up (shortcut k) to the second cell
    print('[Test] Move back up ("k") to second cell')
    notebook_frontend.press("k", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )

    # Move up to the top cell
    print('[Test] Move to top')
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )

    # Move up while already on the top cell and ensure it stays selected
    print('[Test] Move up while already on top')
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )

    # Move down to the last cell + press down to ensure it's still selected
    print('[Test] Move to bottom and press down')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].evaluate(JS_HAS_SELECTED) is True
    )

    # EDIT MODE TESTS

    # Delete all the cells, then add new ones to test
    # arrow key behaviors in edit mode on empty cells
    print('[Test] Prep cells for edit mode tests')
    [notebook_frontend.locate(".fa-cut.fa", page=EDITOR_PAGE).click() for i in range(4)]
    [notebook_frontend.press("b", page=EDITOR_PAGE) for i in range(2)]
    # Add a cell above, which will leave us selected
    # on the third cell out of 4 empty cells
    notebook_frontend.press("a", page=EDITOR_PAGE)

    # Start editing the third empty cell
    print('[Test] Enter edit mode on the third cell')
    notebook_frontend.press("Enter", page=EDITOR_PAGE)
    # Check that the cell is being edited
    notebook_frontend.wait_for_selector('.CodeMirror-focused', page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].locate('.CodeMirror-focused')
    )

    # Arrow up in edit mode on this empty cell (should move to edit move
    # on the cell above when a cell is empty)
    print('[Test] Arrow up in edit mode to the second cell')
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )
    # Type a 1 in edit mode, then arrow left (to the beginning of the cell)
    # and then up, which should then move to edit mode in the cell above
    print('[Test] Enter a "1" in the second cell')
    notebook_frontend.press("1", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowLeft", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True,
    )
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_cells_contents() == ['', '1', '', ''],
    )

    print('[Test] Move to the top cell and edit')
    # Arrow up again while on the top cell, it should still be selected
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )
    # Enter a 0 in the top cell (we're still in edit mode)
    print('[Test] Enter a "0" in the top cell')
    notebook_frontend.press("0", page=EDITOR_PAGE)

    # Move down, right, down, while the edit mode cursor is on the top cell,
    # after the 0 char...this should move down a cell (to the second cell),
    # then right to the end of the 1 char in the second cell, then down to
    # the third empty cell
    print('[Test] Move down to the third cell and edit')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowRight", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    # Put a 2 in the third cell
    print('[Test] Enter a "2" in the third cell')
    notebook_frontend.press("2", page=EDITOR_PAGE)

    # Move down to the last cell, then down again while on the bottom cell
    # (which should stay in the bottom cell), then enter a 3 in the bottom
    # (fourth) cell
    print('[Test] Move down to the bottom cell and edit')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[3].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[3].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.wait_for_condition(  # Ensure it's in edit mode
        lambda: notebook_frontend.cells[3].locate('.CodeMirror-focused'),
    )  # If it's not located, the FrontendElement will be Falsy
    print('[Test] Enter a "3" in the fourth cell')
    notebook_frontend.press("3", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    print('[Test] Check the results match expectations')
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_cells_contents() == ["0", "1", "2", "3"]
    )

    # # Tests in command mode.
    # # Setting up the cells to test the keys to move up.
    # print('[Test] Add some cells')
    # notebook_frontend.to_command_mode()
    # count = 1
    # for _ in range(3):
    #     count += 1
    #     notebook_frontend.press("b", page=EDITOR_PAGE)
    #     notebook_frontend.wait_for_condition(
    #         lambda: len(notebook_frontend.cells) == count
    #     )
    #
    # def await_cell_edit_ready_state(cell_index):
    #     notebook_frontend.wait_for_condition(
    #         lambda: notebook_frontend.cells[cell_index].evaluate(JS_HAS_SELECTED) is True
    #     )
    #     print('/IMG/cell has selected/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    #     codemirror_elem = notebook_frontend.cells[cell_index].locate('.CodeMirror-focused')
    #     if not codemirror_elem or notebook_frontend.cells[cell_index].locate('.CodeMirror-focused').is_visible():
    #         try:
    #             notebook_frontend.wait_for_condition(
    #                 lambda: notebook_frontend.cells[cell_index].locate('.CodeMirror-focused').is_visible()
    #             )
    #         except EndToEndTimeout as err:
    #             pass
    #
    #         print('/IMG/Before enter pressed/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    #         notebook_frontend.press("Enter", page=EDITOR_PAGE)
    #         print('/IMG/keypressed enter/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    #         notebook_frontend.wait_for_condition(
    #             lambda: notebook_frontend.cells[cell_index].locate('.CodeMirror-focused').is_visible()
    #         )
    #         print('/IMG/codemirror is focused/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    #     return True
    #
    # # Use both "k" and up arrow keys to moving up and enter a value.
    # # Once located on the top cell, use the up arrow keys to prove the top cell is still selected.
    # # ............................................
    # print('[Test] Go up and enter "2" in the cell')
    # notebook_frontend.press("k", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(2),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.press("2", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: notebook_frontend.get_cell_contents(index=2) == '2'
    # )
    # notebook_frontend.to_command_mode()
    # # ..................................................
    # print('[Test] Go up and enter "1" in the cell')
    # notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(1),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.press("1", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: notebook_frontend.get_cell_contents(index=1) == '1'
    # )
    # notebook_frontend.to_command_mode()
    # # ............................................
    # print('[Test] Go to top and enter "0" in the cell')
    # print('/IMG/before_arrow_to_top/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    # notebook_frontend.press("k", page=EDITOR_PAGE)
    # notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    # print('/IMG/before_readycheck/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(0),
    #     timeout=330,
    #     period=5
    # )
    # print('/IMG/after_readycheck/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    # notebook_frontend.press("0", page=EDITOR_PAGE)
    # print('/IMG/after_press0/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    # notebook_frontend.wait_for_condition(
    #     lambda: notebook_frontend.get_cell_contents(index=0) == '0'
    # )
    # print('/IMG/cell content is 0/' + notebook_frontend.sshot_edit().hex() + '/IMG/')
    # notebook_frontend.to_command_mode()
    # assert notebook_frontend.get_cells_contents() == ["0", "1", "2", ""]
    #
    # # Use the "k" key on the top cell as well
    # print('[Test] On the top cell, go up again and then edit the cell')
    # notebook_frontend.press("k", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(0),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.type(" edit #1", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", ""]
    #
    # # Setting up the cells to test the keys to move down
    # print('[Test] Arrange/prepare cells')
    # [notebook_frontend.press("j", page=EDITOR_PAGE) for i in range(3)]
    # [notebook_frontend.press("a", page=EDITOR_PAGE) for i in range(2)]
    # notebook_frontend.press("k", page=EDITOR_PAGE)
    #
    # # Use both "j" key and down arrow keys to moving down and enter a value.
    # # Once located on the bottom cell, use the down arrow key to prove the bottom cell is still selected.
    # print('[Test] Go down and input cell values')
    # notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(3),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.press("3", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # notebook_frontend.press("j", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(4),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.press("4", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # notebook_frontend.press("j", page=EDITOR_PAGE)
    # notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(5),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.press("5", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5"]
    #
    # # Use the "j" key on the top cell as well
    # print('[Test] Edit the last cell')
    # notebook_frontend.press("j", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(5),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.type(" edit #1", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5 edit #1"]
    #
    # # On the bottom cell, use both left and right arrow keys to prove the bottom cell is still selected.
    # notebook_frontend.press("ArrowLeft", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(6),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.type(", #2", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5 edit #1, #2"]
    # notebook_frontend.press("ArrowRight", page=EDITOR_PAGE)
    # notebook_frontend.wait_for_condition(
    #     lambda: await_cell_edit_ready_state(6),
    #     timeout=330,
    #     period=5
    # )
    # notebook_frontend.type(" and #3", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # assert notebook_frontend.get_cells_contents() == ["0 edit #1", "1", "2", "3", "4", "5 edit #1, #2 and #3"]
    #
    # # Tests in edit mode.
    # # First, erase the previous content and then setup the cells to test the keys to move up.
    # [notebook_frontend.locate(".fa-cut.fa", page=EDITOR_PAGE).click() for i in range(6)]
    # [notebook_frontend.press("b", page=EDITOR_PAGE) for i in range(2)]
    # notebook_frontend.press("a", page=EDITOR_PAGE)
    # notebook_frontend.press("Enter", page=EDITOR_PAGE)
    #
    # # Use the up arrow key to move down and enter a value.
    # # We will use the left arrow key to move one char to the left since moving up on last character only moves selector to the first one.
    # # Once located on the top cell, use the up arrow key to prove the top cell is still selected.
    # notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    # notebook_frontend.press("1", page=EDITOR_PAGE)
    # notebook_frontend.press("ArrowLeft", page=EDITOR_PAGE)
    # [notebook_frontend.press("ArrowUp", page=EDITOR_PAGE) for i in range(2)]
    # notebook_frontend.press("0", page=EDITOR_PAGE)
    #
    # # Use the down arrow key to move down and enter a value.
    # # We will use the right arrow key to move one char to the right since moving down puts selector to the last character.
    # # Once located on the bottom cell, use the down arrow key to prove the bottom cell is still selected.
    # notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    # notebook_frontend.press("ArrowRight", page=EDITOR_PAGE)
    # notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    # notebook_frontend.press("2", page=EDITOR_PAGE)
    # [notebook_frontend.press("ArrowDown", page=EDITOR_PAGE) for i in range(2)]
    # notebook_frontend.press("3", page=EDITOR_PAGE)
    # notebook_frontend.to_command_mode()
    # assert notebook_frontend.get_cells_contents() == ["0", "1", "2", "3"]
