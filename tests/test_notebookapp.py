import json


async def test_tree_handler(fetch, notebookapp):
    r = await fetch('tree')
    assert r.code == 200


# async def test_notebook_handler(fetch, notebookapp):
#     r = await fetch('notebooks')
#     assert r.code == 200

