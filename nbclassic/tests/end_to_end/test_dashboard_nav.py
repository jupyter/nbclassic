"""Test navigation to directory links"""


import os

from .utils import  TREE_PAGE
from jupyter_server.utils import url_path_join
pjoin = os.path.join


def url_in_tree(nb, url=None):
    if url is None:
        url = nb.get_page_url(page=TREE_PAGE)

    tree_url = url_path_join(nb.get_server_info(), 'tree')
    return True if tree_url in url else False


def get_list_items(nb):
    """
    Gets list items from a directory listing page
    """

    nb.wait_for_selector('#notebook_list .item_link', page=TREE_PAGE)
    notebook_list = nb.locate('#notebook_list', page=TREE_PAGE)
    link_items = notebook_list.locate_all('.item_link')

    return [{
        'link': a.get_attribute('href'),
        'label': a.get_inner_text(),
        'element': a,
    } for a in link_items if a.get_inner_text() != '..']


def test_navigation(notebook_frontend):
    print('[Test] [test_dashboard_nav] Start!')

    print('[Test] Obtain list of elements')
    link_elements = get_list_items(notebook_frontend)

    # Recursively traverse and check folder in the Jupyter root dir
    def check_links(nb, list_of_link_elements):
        print('[Test] Check links')
        if len(list_of_link_elements) < 1:
            return

        for item in list_of_link_elements:
            print(f'[Test]   Check "{item["label"]}"')
            if 'Untitled.ipynb' in item["label"]:
                # Skip notebook files in the temp dir
                continue

            item["element"].click()

            notebook_frontend.wait_for_condition(
                lambda: url_in_tree(notebook_frontend),
                timeout=600,
                period=5
            )
            notebook_frontend.wait_for_condition(
                lambda: item["link"] in nb.get_page_url(page=TREE_PAGE),
                timeout=600,
                period=5
            )

            new_links = get_list_items(nb)
            if len(new_links) > 0:
                check_links(nb, new_links)

            nb.go_back(page=TREE_PAGE)

        return

    check_links(notebook_frontend, link_elements)
    print('[Test] [test_dashboard_nav] Finished!')
