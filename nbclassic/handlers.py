"""Module to patch in Extension Handler 
"""

from jupyter_server.extension.handler import ExtensionHandler
from notebook.tree.handlers import (
    TreeHandler,
    default_handlers as tree_default_handlers
)
from notebook.notebook.handlers import (
    NotebookHandler,
    default_handlers as notebook_default_handlers
)

class BaseHandler:
    
    def get_template(self, name):
        """Return the jinja template object for a given name"""
        template_env = "{}_jinja2_env".format(self.extension_name)
        return self.settings[template_env].get_template(name)

class ShimmedNotebookHandler(BaseHandler, ExtensionHandler, NotebookHandler): pass

class ShimmedTreeHandler(BaseHandler, ExtensionHandler, TreeHandler): pass

tree_default_handlers = [
    (path, ShimmedTreeHandler) 
    for (path, handler) in tree_default_handlers
]

notebook_default_handlers = [
    (path, ShimmedNotebookHandler) 
    for (path, handler) in notebook_default_handlers
]

default_handlers = tree_default_handlers + notebook_default_handlers