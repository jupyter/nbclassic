import os
from tkinter.tix import NoteBook
from turtle import home
from .utils import EDITOR_PAGE, TREE_PAGE
from jupyter_server.utils import url_path_join
pjoin = os.path.join


class PageError(Exception):
    """Error for an action being incompatible with the current jupyter web page."""
    def __init__(self, message):
        self.message = message


def url_in_tree(browser, url=None):
    if url is None:
        url = browser.pages[0].url

    tree_url = url_path_join(browser.jupyter_server_info['url'], 'tree')
    return True if tree_url in url else False


def get_list_items(browser):
    """Gets list items from a directory listing page

    Raises PageError if not in directory listing page (url has tree in it)
    """
    if not url_in_tree(browser):
        raise PageError("You are not in the notebook's file tree view."
                        "This function can only be used the file tree context.")

    browser.pages[0].wait_for_selector('.item_link')

    return [{
        'link': a.get_attribute('href'),
        'label': a.inner_text(),
        'element': a,
    } for a in browser.pages[0].query_selector_all('.item_link')]

def only_dir_links(browser):
    """Return only links that point at other directories in the tree"""

    items = get_list_items(browser)
    
    return [i for i in items 
            if url_in_tree(browser, i['link']) and i['label'] != '..']

def test_items(notebook_frontend):
    authenticated_browser = notebook_frontend.get_browser_context()

    home_page = notebook_frontend.get_browser_page(page=TREE_PAGE)
    visited_dict = {}

    while True:
        home_page.wait_for_selector('.item_link')

        # store the links to directories available in this current URL. URL is the key, the list of directory URLs is the value
        items = visited_dict[home_page.url] = only_dir_links(authenticated_browser)

        try: 
            # Access the first link in the list
            item = items[0]

            # Click on the link
            item["element"].click()
            # Make sure we navigate to that link
            assert home_page.url == item['link']
        except IndexError:
            break

    # Going back up the tree while we still have unvisited links
    while visited_dict:
        # Generate a list of directory links from the home URL 
        current_items = only_dir_links(authenticated_browser)

        # Save each link from the current_items list into this new variable
        current_items_links = [item["link"] for item in current_items]

        # If the current URL we are at, is in the visited_dict, remove it
        stored_items = visited_dict.pop(home_page.url)

        # Store that visted URL in the stored_items_links list
        stored_items_links = [item["link"] for item in stored_items]

        assert stored_items_links == current_items_links

        home_page.go_back()
