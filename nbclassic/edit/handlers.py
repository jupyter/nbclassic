#encoding: utf-8
"""Tornado handlers for the terminal emulator."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tornado import web, gen
from jupyter_server.base.handlers import JupyterHandler, path_regex
from jupyter_server.utils import url_path_join, url_escape, ensure_async
from jupyter_server.extension.handler import (
    ExtensionHandlerMixin,
    ExtensionHandlerJinjaMixin
)

class EditorHandler(ExtensionHandlerJinjaMixin, ExtensionHandlerMixin, JupyterHandler):
    """Render the text editor interface."""

    @web.authenticated
    @gen.coroutine
    def get(self, path):
        if (self.contents_manager.dir_exists(path)):
            # it's a *directory*, redirect to /tree
            url = url_path_join(self.base_url, 'tree', url_escape(path))
            self.redirect(url)
        else:
            path = path.strip('/')
            if not (self.contents_manager.file_exists(path)):
                raise web.HTTPError(404, u'File does not exist: %s' % path)

            basename = path.rsplit('/', 1)[-1]
            self.write(self.render_template('edit.html',
                file_path=url_escape(path),
                basename=basename,
                page_title=basename + " (editing)",
                )
            )

default_handlers = [
    (r"/edit%s" % path_regex, EditorHandler),
]
