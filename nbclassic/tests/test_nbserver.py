import pytest


def test_classic_notebook_templates(jp_serverapp):
    classic_notebook_templates = [
        "notebook.html",
        "tree.html"
    ]
    # Get the server's template environment.
    template_env = jp_serverapp.web_app.settings.get("notebook_jinja2_env")

    for name in classic_notebook_templates:
        template_env.get_template(name)


async def test_classic_notebook_asset_URLS(jp_fetch):
    classic_notebook_paths = [
        # Some classic notebook asset paths
        '/static/notebook/js/main.js',
        '/static/services/contents.js',
        # NBclassic asset paths work too.
        '/static/notebook/notebook/js/main.js',
        '/static/notebook/services/contents.js',
    ]

    for url_path in classic_notebook_paths:
        r = await jp_fetch(url_path)
        assert r.code == 200
