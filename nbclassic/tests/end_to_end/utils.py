import datetime
import os
import time
from contextlib import contextmanager
from os.path import join as pjoin

from playwright.sync_api import ElementHandle, JSHandle

# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.remote.webelement import WebElement


# Key constants for browser_data
BROWSER = 'BROWSER'
TREE_PAGE = 'TREE_PAGE'
EDITOR_PAGE = 'EDITOR_PAGE'
SERVER_INFO = 'SERVER_INFO'
BROWSER_RAW = 'BROWSER_RAW'
# Other constants
CELL_OUTPUT_SELECTOR = '.output_subarea'


# def wait_for_selector(driver, selector, timeout=10, visible=False, single=False, wait_for_n=1, obscures=False):
#     if wait_for_n > 1:
#         return _wait_for_multiple(
#             driver, By.CSS_SELECTOR, selector, timeout, wait_for_n, visible)
#     return _wait_for(driver, By.CSS_SELECTOR, selector, timeout, visible, single, obscures)
#
#
# def wait_for_tag(driver, tag, timeout=10, visible=False, single=False, wait_for_n=1, obscures=False):
#     if wait_for_n > 1:
#         return _wait_for_multiple(
#             driver, By.TAG_NAME, tag, timeout, wait_for_n, visible)
#     return _wait_for(driver, By.TAG_NAME, tag, timeout, visible, single, obscures)
#
#
# def wait_for_xpath(driver, xpath, timeout=10, visible=False, single=False, wait_for_n=1, obscures=False):
#     if wait_for_n > 1:
#         return _wait_for_multiple(
#             driver, By.XPATH, xpath, timeout, wait_for_n, visible)
#     return _wait_for(driver, By.XPATH, xpath, timeout, visible, single, obscures)
#
#
# def wait_for_script_to_return_true(driver, script, timeout=10):
#     WebDriverWait(driver, timeout).until(lambda d: d.execute_script(script))
#
#
# def _wait_for(driver, locator_type, locator, timeout=10, visible=False, single=False, obscures=False):
#     """Waits `timeout` seconds for the specified condition to be met. Condition is
#     met if any matching element is found. Returns located element(s) when found.
#
#     Args:
#         driver: Selenium web driver instance
#         locator_type: type of locator (e.g. By.CSS_SELECTOR or By.TAG_NAME)
#         locator: name of tag, class, etc. to wait for
#         timeout: how long to wait for presence/visibility of element
#         visible: if True, require that element is not only present, but visible
#         single: if True, return a single element, otherwise return a list of matching
#         elements
#         obscures: if True, waits until the element becomes invisible
#     """
#     wait = WebDriverWait(driver, timeout)
#     if obscures:
#         conditional = EC.invisibility_of_element_located
#     elif single:
#         if visible:
#             conditional = EC.visibility_of_element_located
#         else:
#             conditional = EC.presence_of_element_located
#     else:
#         if visible:
#             conditional = EC.visibility_of_all_elements_located
#         else:
#             conditional = EC.presence_of_all_elements_located
#     return wait.until(conditional((locator_type, locator)))
#
#
# def _wait_for_multiple(driver, locator_type, locator, timeout, wait_for_n, visible=False):
#     """Waits until `wait_for_n` matching elements to be present (or visible).
#     Returns located elements when found.
#
#     Args:
#         driver: Selenium web driver instance
#         locator_type: type of locator (e.g. By.CSS_SELECTOR or By.TAG_NAME)
#         locator: name of tag, class, etc. to wait for
#         timeout: how long to wait for presence/visibility of element
#         wait_for_n: wait until this number of matching elements are present/visible
#         visible: if True, require that elements are not only present, but visible
#     """
#     wait = WebDriverWait(driver, timeout)
#
#     def multiple_found(driver):
#         elements = driver.find_elements(locator_type, locator)
#         if visible:
#             elements = [e for e in elements if e.is_displayed()]
#         if len(elements) < wait_for_n:
#             return False
#         return elements
#
#     return wait.until(multiple_found)


class TimeoutError(Exception):

    def get_result(self):
        return None if not self.args else self.args[0]


class CellTypeError(ValueError):

    def __init__(self, message=""):
        self.message = message


class FrontendError(Exception):
    pass


class NotebookFrontend:

    # Some constants for users of the class
    TREE_PAGE = TREE_PAGE
    EDITOR_PAGE = EDITOR_PAGE
    CELL_OUTPUT_SELECTOR = CELL_OUTPUT_SELECTOR

    CELL_INDEX = 'INDEX'
    CELL_TEXT = 'TEXT'
    _CELL_DATA_FORMAT = {
        CELL_INDEX: None,  # int
        CELL_TEXT: None,  # str
    }

    def __init__(self, browser_data, existing_file_name=None):
        # Keep a reference to source data
        self._browser_data = browser_data

        # Define tree and editor attributes
        self.tree_page = browser_data[TREE_PAGE]
        self.editor_page = self._open_notebook_editor_page(existing_file_name)

        # Do some needed frontend setup
        self._wait_for_start()
        self.disable_autosave_and_onbeforeunload()  # TODO fix/refactor
        self.current_cell = None  # Defined/used below  # TODO refactor/remove

    # def __len__(self):
    #     return len(self._cells)
    #
    # def __getitem__(self, key):
    #     return self._cells[key]
    #
    # def __setitem__(self, key, item):
    #     if isinstance(key, int):
    #         self.edit_cell(index=key, content=item, render=False)
    #     # TODO: re-add slicing support, handle general python slicing behaviour
    #     # includes: overwriting the entire self._cells object if you do
    #     # self[:] = []
    #     # elif isinstance(key, slice):
    #     #     indices = (self.index(cell) for cell in self[key])
    #     #     for k, v in zip(indices, item):
    #     #         self.edit_cell(index=k, content=v, render=False)
    #
    # def __iter__(self):
    #     return (cell for cell in self._cells)

    def _wait_for_start(self):
        """Wait until the notebook interface is loaded and the kernel started"""
        # wait_for_selector(self.browser, '.cell')
        self.tree_page.locator('.cell')

        def check_is_kernel_running():
            return (self.is_jupyter_defined()
                    and self.is_notebook_defined()
                    and self.is_kernel_running())

        self._wait_for_condition(check_is_kernel_running)

    @property
    def body(self):
        return self.editor_page.locator("body")

    @property
    def _cells(self):
        """Gets all cells once they are visible.

        """
        return self.editor_page.query_selector_all(".cell")

    @property
    def cells(self):
        """Gets all cells once they are visible."""
        # self.cells is now a list of dicts containing info per-cell
        # (self._cells returns cell objects, should not be used externally)

        # This mirrors the self._CELL_DATA_FORMAT
        cell_dicts = [
            {self.CELL_INDEX: index, self.CELL_TEXT: cell.inner_text()}
            for index, cell in enumerate(self._cells)
        ]

        return cell_dicts

    @property
    def current_index(self):
        return self.index(self.current_cell)

    def index(self, cell):
        return self._cells.index(cell)

    def press(self, keycode, page, modifiers=None):
        if page == TREE_PAGE:
            specified_page = self.tree_page
        elif page == EDITOR_PAGE:
            specified_page = self.editor_page
        else:
            raise Exception('Error, provide a valid page to evaluate from!')

        mods = ""
        if modifiers is not None:
            mods = "+".join(m for m in modifiers)
            mods += "+"

        specified_page.keyboard.press(mods + keycode)

    def type(self, text, page):
        if page == TREE_PAGE:
            specified_page = self.tree_page
        elif page == EDITOR_PAGE:
            specified_page = self.editor_page
        else:
            raise Exception('Error, provide a valid page to evaluate from!')
        specified_page.keyboard.type(text)

    def press_active(self, keycode, modifiers=None):
        mods = ""
        if modifiers is not None:
            mods = "+".join(m for m in modifiers)

        self.current_cell.press(mods + "+" + keycode)

    def type_active(self, text):
        self.current_cell.type(text)

    def try_click_selector(self, selector, page):
        if page == TREE_PAGE:
            specified_page = self.tree_page
        elif page == EDITOR_PAGE:
            specified_page = self.editor_page
        else:
            raise Exception('Error, provide a valid page to evaluate from!')
        elem = specified_page.locator(selector)

        elem.click()

    # def wait_for_selector(self, selector, page):
    #     if page == TREE_PAGE:
    #         specified_page = self.tree_page
    #     elif page == EDITOR_PAGE:
    #         specified_page = self.editor_page
    #     else:
    #         raise Exception('Error, provide a valid page to evaluate from!')
    #     elem = specified_page.locator(selector)

    def get_platform_modifier_key(self):
        """Jupyter Notebook uses different modifier keys on win (Control) vs mac (Meta)"""
        if os.uname()[0] == "Darwin":
            return "Meta"
        else:
            return "Control"

    def evaluate(self, text, page):
        if page == TREE_PAGE:
            specified_page = self.tree_page
        elif page == EDITOR_PAGE:
            specified_page = self.editor_page
        else:
            raise Exception('Error, provide a valid page to evaluate from!')

        return specified_page.evaluate(text)

    def _pause(self):
        self.editor_page.pause()

    def wait_for_tag(self, tag, page=None, cell_index=None):
        if cell_index is None and page is None:
            raise FrontendError('Provide a page or cell to wait from!')
        if cell_index is not None and page is not None:
            raise FrontendError('Provide only one of [page, cell] to wait from!')

        result = None
        if page is not None:
            if page == TREE_PAGE:
                specified_page = self.tree_page
            elif page == EDITOR_PAGE:
                specified_page = self.editor_page
            else:
                raise Exception('Error, provide a valid page to evaluate from!')

            result = specified_page.locator(tag)
        if cell_index is not None:
            result = self._cells[cell_index].wait_for_selector(tag)

        return result

    def _locate(self, selector, page):
        result = None
        if page == TREE_PAGE:
            specified_page = self.tree_page
        elif page == EDITOR_PAGE:
            specified_page = self.editor_page
        else:
            raise Exception('Error, provide a valid page to evaluate from!')

        return specified_page.locator(selector)

    def clear_all_output(self):
        return self.evaluate(
            "Jupyter.notebook.clear_all_output();",
            page=EDITOR_PAGE
        )

    def clear_cell_output(self, index):
        JS = f'Jupyter.notebook.clear_output({index})'
        self.evaluate(JS, page=EDITOR_PAGE)

    def delete_all_cells(self):
        # Note: After deleting all cells, a single default cell will remain

        for _ in range(len(self._cells)):
            self.delete_cell(0)

    def populate(self, cell_texts):
        """Delete all cells, then add cells using the list of specified cell_texts"""
        self.delete_all_cells()

        for _ in range(len(cell_texts) - 1):  # Remove 1, there will already be 1 default cell
            self.add_cell()
        for index, txt in enumerate(cell_texts):
            self.edit_cell(None, index, txt)

    def click_toolbar_execute_btn(self):
        execute_button = self.editor_page.locator(
            "button["
                "data-jupyter-action="
                    "'jupyter-notebook:run-cell-and-select-next'"
            "]"
        )
        execute_button.click()

    def disable_autosave_and_onbeforeunload(self):
        """Disable request to save before closing window and autosave.

        This is most easily done by using js directly.
        """
        self.evaluate("window.onbeforeunload = null;", page=EDITOR_PAGE)
        self.evaluate("Jupyter.notebook.set_autosave_interval(0)", page=EDITOR_PAGE)

    def to_command_mode(self):
        """Changes us into command mode on currently focused cell"""
        self.body.press('Escape')
        self.evaluate(" () => { return Jupyter.notebook.handle_command_mode("
                                       "Jupyter.notebook.get_cell("
                                           "Jupyter.notebook.get_edit_index())) }", page=EDITOR_PAGE)

    def focus_cell(self, index=0):
        cell = self._cells[index]
        cell.click()
        self.to_command_mode()
        self.current_cell = cell

    def select_cell_range(self, initial_index=0, final_index=0):
        self.focus_cell(initial_index)
        self.to_command_mode()
        for i in range(final_index - initial_index):
            self.press('j', EDITOR_PAGE, ['Shift'])

    def find_and_replace(self, index=0, find_txt='', replace_txt=''):
        self.focus_cell(index)
        self.to_command_mode()
        self.press('f', EDITOR_PAGE)
        self.editor_page.locator('#find-and-replace')
        self.editor_page.locator('#findreplace_allcells_btn').click()
        self.editor_page.locator('#findreplace_find_inp').type(find_txt)
        self.editor_page.locator('#findreplace_replace_inp').type(replace_txt)
        self.editor_page.locator('#findreplace_replaceall_btn').click()

    def convert_cell_type(self, index=0, cell_type="code"):
        # TODO add check to see if it is already present
        self.focus_cell(index)
        cell = self._cells[index]
        if cell_type == "markdown":
            self.current_cell.press("m")
        elif cell_type == "raw":
            self.current_cell.press("r")
        elif cell_type == "code":
            self.current_cell.press("y")
        else:
            raise CellTypeError(f"{cell_type} is not a valid cell type,use 'code', 'markdown', or 'raw'")

        self._wait_for_stale_cell(cell)
        self.focus_cell(index)
        return self.current_cell

    def _wait_for_stale_cell(self, cell):
        """ This is needed to switch a cell's mode and refocus it, or to render it.

        Warning: there is currently no way to do this when changing between
        markdown and raw cells.
        """
        # wait = WebDriverWait(self.browser, 10)
        # element = wait.until(EC.staleness_of(cell))

        cell.wait_for_element_state('hidden')

    # def wait_for_element_availability(self, element):
    #     _wait_for(self.browser, By.CLASS_NAME, element, visible=True)

    def get_cells_contents(self):
        JS = '() => { return Jupyter.notebook.get_cells().map(function(c) {return c.get_text();}) }'
        return self.evaluate(JS, page=EDITOR_PAGE)

    def get_cell_contents(self, index=0, selector='div .CodeMirror-code'):
        return self._cells[index].query_selector(selector).inner_text()

    def get_cell_output(self, index=0, output=CELL_OUTPUT_SELECTOR):
        cell = self._cells[index].as_element().query_selector(output)  # Find cell child elements

        if cell is None:
            return None

        cell_data = dict(self._CELL_DATA_FORMAT)
        cell_data[self.CELL_INDEX] = index
        cell_data[self.CELL_TEXT] = cell.inner_text()

        return cell_data

    def _wait_for_condition(self, check_func, timeout=30, period=.1):
        """Wait for check_func to return a truthy value, return it or raise an exception upon timeout"""
        # TODO refactor/remove

        begin = datetime.datetime.now()
        while (datetime.datetime.now() - begin).seconds < timeout:
            condition = check_func()
            if condition:
                return condition
            time.sleep(period)
        else:
            raise TimeoutError()

    def wait_for_cell_output(self, index=0, timeout=3):
        if not self._cells:
            raise Exception('Error, no cells exist!')

        milliseconds_to_seconds = 1000
        cell = self._cells[index].as_element()
        try:
            cell.wait_for_selector(CELL_OUTPUT_SELECTOR, timeout=timeout * milliseconds_to_seconds)
        except Exception:
            # None were found / timeout
            pass

        return self.get_cell_output(index=index)

    def set_cell_metadata(self, index, key, value):
        JS = f'Jupyter.notebook.get_cell({index}).metadata.{key} = {value}'
        return self.evaluate(JS, page=EDITOR_PAGE)

    def get_cell_type(self, index=0):
        JS = f'() => {{ return Jupyter.notebook.get_cell({index}).cell_type }}'
        return self.evaluate(JS, page=EDITOR_PAGE)

    def set_cell_input_prompt(self, index, prmpt_val):
        JS = f'Jupyter.notebook.get_cell({index}).set_input_prompt({prmpt_val})'
        self.evaluate(JS, page=EDITOR_PAGE)

    # TODO refactor this, it's terrible
    def edit_cell(self, cell=None, index=0, content="", render=False):
        """Set the contents of a cell to *content*, by cell object or by index
        """
        if cell is not None:
            index = self.index(cell)
        self.focus_cell(index)

        # Select & delete anything already in the cell
        self.press('Enter', EDITOR_PAGE)
        self.press('a', EDITOR_PAGE, [self.get_platform_modifier_key()])
        self.press('Delete', EDITOR_PAGE)

        self.type(content, page=EDITOR_PAGE)
        # TODO cleanup
        # for line_no, line in enumerate(content.splitlines()):
        #     if line_no != 0:
        #         self.editor_page.keyboard.press("Enter")
        #     self.editor_page.keyboard.press("Enter")
        #     self.editor_page.keyboard.type(line)
        if render:
            self.execute_cell(index)

    def execute_cell(self, cell_or_index=None):
        if isinstance(cell_or_index, int):
            index = cell_or_index
        elif isinstance(cell_or_index, ElementHandle):
            # TODO: This probably doesn't work, fix/check
            index = self.index(cell_or_index)
        else:
            raise TypeError("execute_cell only accepts an ElementHandle or an int")
        self.focus_cell(index)
        self.current_cell.press("Control+Enter")

    def add_cell(self, index=-1, cell_type="code", content=""):
        # TODO fix/respect cell_type arg
        self.focus_cell(index)
        self.current_cell.press("b")
        new_index = index + 1 if index >= 0 else index
        if content:
            self.edit_cell(index=index, content=content)
        # TODO fix this
        if cell_type != 'code':
            # raise NotImplementedError('Error, non code cell_type is a TODO!')
            self.convert_cell_type(index=new_index, cell_type=cell_type)

    # def add_and_execute_cell(self, index=-1, cell_type="code", content=""):
    #     self.add_cell(index=index, cell_type=cell_type, content=content)
    #     self.execute_cell(index)

    def delete_cell(self, index):
        self.focus_cell(index)
        self.to_command_mode()
        self.current_cell.type('dd')

    def add_markdown_cell(self, index=-1, content="", render=True):
        self.add_cell(index, cell_type="markdown")
        self.edit_cell(index=index, content=content, render=render)

    def append(self, *values, cell_type="code"):
        for value in values:
            if isinstance(value, str):
                self.add_cell(cell_type=cell_type,
                              content=value)
            else:
                raise TypeError(f"Don't know how to add cell from {value!r}")

    # def extend(self, values):
    #     self.append(*values)
    #
    # def run_all(self):
    #     for cell in self:
    #         self.execute_cell(cell)
    #
    # def trigger_keydown(self, keys):
    #     trigger_keystrokes(self.body, keys)

    def is_jupyter_defined(self):
        """Checks that the Jupyter object is defined on the frontend"""
        return self.evaluate(
            "() => {"
            "  try {"
            "    return Jupyter != false;"
            "  } catch (e) {"
            "    return false;"
            "  }"
            "}",
            page=EDITOR_PAGE
        )

    def is_notebook_defined(self):
        """Checks that the Jupyter.notebook object is defined on the frontend"""
        return self.evaluate(
            "() => {"
            "  try {"
            "    return Jupyter.notebook != false;"
            "  } catch (e) {"
            "    return false;"
            "  }"
            "}",
            page=EDITOR_PAGE
        )

    def is_kernel_running(self):
        return self.evaluate(
            "() => { return Jupyter.notebook.kernel && Jupyter.notebook.kernel.is_connected() }",
            page=EDITOR_PAGE
        )

    def wait_for_kernel_ready(self):
        self.tree_page.locator(".kernel_idle_icon")

    def _open_notebook_editor_page(self, existing_file_name=None):
        tree_page = self.tree_page
        
        if existing_file_name is not None:
            existing_notebook = tree_page.locator('div.list_item:nth-child(4) > div:nth-child(1) > a:nth-child(3)')
            existing_notebook.click()
            self.tree_page.reload()  # TODO: FIX this, page count does not update to 2
        else:
            # Simulate a user opening a new notebook/kernel
            new_dropdown_element = tree_page.locator('#new-dropdown-button')
            new_dropdown_element.click()
            kernel_name = 'kernel-python3'
            kernel_selector = f'#{kernel_name} a'
            new_notebook_element = tree_page.locator(kernel_selector)
            new_notebook_element.click()

        def wait_for_new_page():
            return [pg for pg in self._browser_data[BROWSER].pages if 'tree' not in pg.url]

        new_pages = self._wait_for_condition(wait_for_new_page)
        editor_page = new_pages[0]

        return editor_page

    # TODO: Refactor/consider removing this
    @classmethod
    def new_notebook_frontend(cls, browser_data, kernel_name='kernel-python3', existing_file_name=None):
        browser = browser_data[BROWSER]
        tree_page = browser_data[TREE_PAGE]
        server_info = browser_data[SERVER_INFO]

        # with new_window(page):
        # select_kernel(tree_page, kernel_name=kernel_name)  # TODO this is terrible, remove it
        # tree_page.pause()
        instance = cls(browser_data, existing_file_name)

        return instance


# # TODO: refactor/remove this
# def select_kernel(page, kernel_name='kernel-python3'):
#     """Clicks the "new" button and selects a kernel from the options.
#     """
#     # wait = WebDriverWait(browser, 10)
#     # new_button = wait.until(EC.element_to_be_clickable((By.ID, "new-dropdown-button")))
#     new_button = page.locator('#new-dropdown-button')
#     new_button.click()
#     kernel_selector = f'#{kernel_name} a'
#     # kernel = wait_for_selector(page, kernel_selector, single=True)
#     kernel = page.locator(kernel_selector)
#     kernel.click()


# @contextmanager
# def new_window(browser):
#     """Contextmanager for switching to & waiting for a window created.
#
#     This context manager gives you the ability to create a new window inside
#     the created context and it will switch you to that new window.
#
#     Usage example:
#
#         from nbclassic.tests.selenium.utils import new_window, Notebook
#
#         ⋮ # something that creates a browser object
#
#         with new_window(browser):
#             select_kernel(browser, kernel_name=kernel_name)
#         nb = Notebook(browser)
#
#     """
#     initial_window_handles = browser.window_handles
#     yield
#     new_window_handles = [window for window in browser.window_handles
#                           if window not in initial_window_handles]
#     if not new_window_handles:
#         raise Exception("No new windows opened during context")
#     browser.switch_to.window(new_window_handles[0])


# def shift(browser, k):
#     """Send key combination Shift+(k)"""
#     trigger_keystrokes(browser, "shift-%s"%k)


# def cmdtrl(page, key):
#     """Send key combination Ctrl+(key) or Command+(key) for MacOS"""
#     if os.uname()[0] == "Darwin":
#         page.keyboard.press("Meta+{}".format(key))
#     else:
#         page.keyboard.press("Control+{}".format(key))


# def alt(browser, k):
#     """Send key combination Alt+(k)"""
#     trigger_keystrokes(browser, 'alt-%s'%k)
#
#
# def trigger_keystrokes(browser, *keys):
#     """ Send the keys in sequence to the browser.
#     Handles following key combinations
#     1. with modifiers eg. 'control-alt-a', 'shift-c'
#     2. just modifiers eg. 'alt', 'esc'
#     3. non-modifiers eg. 'abc'
#     Modifiers : http://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html
#     """
#     for each_key_combination in keys:
#         keys = each_key_combination.split('-')
#         if len(keys) > 1:  # key has modifiers eg. control, alt, shift
#             modifiers_keys = [getattr(Keys, x.upper()) for x in keys[:-1]]
#             ac = ActionChains(browser)
#             for i in modifiers_keys: ac = ac.key_down(i)
#             ac.send_keys(keys[-1])
#             for i in modifiers_keys[::-1]: ac = ac.key_up(i)
#             ac.perform()
#         else:              # single key stroke. Check if modifier eg. "up"
#             browser.send_keys(getattr(Keys, keys[0].upper(), keys[0]))
#
#
# def validate_dualmode_state(notebook, mode, index):
#     '''Validate the entire dual mode state of the notebook.
#     Checks if the specified cell is selected, and the mode and keyboard mode are the same.
#     Depending on the mode given:
#         Command: Checks that no cells are in focus or in edit mode.
#         Edit:    Checks that only the specified cell is in focus and in edit mode.
#     '''
#     def is_only_cell_edit(index):
#         JS = 'return Jupyter.notebook.get_cells().map(function(c) {return c.mode;})'
#         cells_mode = notebook.browser.execute_script(JS)
#         #None of the cells are in edit mode
#         if index is None:
#             for mode in cells_mode:
#                 if mode == 'edit':
#                     return False
#             return True
#         #Only the index cell is on edit mode
#         for i, mode in enumerate(cells_mode):
#             if i == index:
#                 if mode != 'edit':
#                     return False
#             else:
#                 if mode == 'edit':
#                     return False
#         return True
#
#     def is_focused_on(index):
#         JS = "return $('#notebook .CodeMirror-focused textarea').length;"
#         focused_cells = notebook.browser.execute_script(JS)
#         if index is None:
#             return focused_cells == 0
#
#         if focused_cells != 1: #only one cell is focused
#             return False
#
#         JS = "return $('#notebook .CodeMirror-focused textarea')[0];"
#         focused_cell = notebook.browser.execute_script(JS)
#         JS = "return IPython.notebook.get_cell(%s).code_mirror.getInputField()"%index
#         cell = notebook.browser.execute_script(JS)
#         return focused_cell == cell
#
#     #general test
#     JS = "return IPython.keyboard_manager.mode;"
#     keyboard_mode = notebook.browser.execute_script(JS)
#     JS = "return IPython.notebook.mode;"
#     notebook_mode = notebook.browser.execute_script(JS)
#
#     #validate selected cell
#     JS = "return Jupyter.notebook.get_selected_cells_indices();"
#     cell_index = notebook.browser.execute_script(JS)
#     assert cell_index == [index] #only the index cell is selected
#
#     if mode != 'command' and mode != 'edit':
#         raise Exception('An unknown mode was send: mode = "%s"'%mode) #An unknown mode is send
#
#     #validate mode
#     assert mode == keyboard_mode #keyboard mode is correct
#
#     if mode == 'command':
#         assert is_focused_on(None) #no focused cells
#
#         assert is_only_cell_edit(None) #no cells in edit mode
#
#     elif mode == 'edit':
#         assert is_focused_on(index) #The specified cell is focused
#
#         assert is_only_cell_edit(index) #The specified cell is the only one in edit mode
