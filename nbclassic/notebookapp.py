# coding: utf-8
"""A tornado based Jupyter notebook server."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import absolute_import, print_function

import os
import gettext
import random
import sys
import warnings
import gettext

from jinja2 import Environment, FileSystemLoader

import notebook
from notebook import (
    DEFAULT_STATIC_FILES_PATH,
    DEFAULT_TEMPLATE_PATH_LIST,
    __version__,
)

from traitlets.config import Config
from traitlets.config.application import boolean_flag
from traitlets import (
    Dict, Unicode, Integer, List, Bool,
    observe, default
)
from ipython_genutils import py3compat
from jupyter_core.paths import jupyter_path

from jupyter_server.base.handlers import FileFindHandler
from jupyter_server.utils import url_path_join

# Try to load Notebook as an extension of the Jupyter Server
from jupyter_server.extension.application import (
    ExtensionApp,
    ExtensionAppJinjaMixin
)

from jupyter_server.log import log_request
from jupyter_server.transutils import _
from jupyter_server.serverapp import (
    ServerApp,
    random_ports,
    load_handlers
)
from jupyter_server.utils import url_path_join as ujoin

from .terminal.handlers import TerminalHandler


#-----------------------------------------------------------------------------
# Module globals
#-----------------------------------------------------------------------------

_examples = """
jupyter nbclassic                       # start the notebook
jupyter nbclassic --certfile=mycert.pem # use SSL/TLS certificate
jupyter nbclassic password              # enter a password to protect the server
"""

#-----------------------------------------------------------------------------
# Aliases and Flags
#-----------------------------------------------------------------------------

flags = {}
aliases = {}
flags['no-browser']=(
    {'ServerApp' : {'open_browser' : False}},
    _("Don't open the notebook in a browser after startup.")
)
flags['no-mathjax']=(
    {'NotebookApp' : {'enable_mathjax' : False}},
    """Disable MathJax

    MathJax is the javascript library Jupyter uses to render math/LaTeX. It is
    very large, so you may want to disable it if you have a slow internet
    connection, or for offline use of the notebook.

    When disabled, equations etc. will appear as their untransformed TeX source.
    """
)

flags['allow-root']=(
    {'ServerApp' : {'allow_root' : True}},
    _("Allow the notebook to be run from root user.")
)

aliases.update({
    'ip': 'ServerApp.ip',
    'port': 'ServerApp.port',
    'port-retries': 'ServerApp.port_retries',
    #'transport': 'KernelManager.transport',
    'keyfile': 'ServerApp.keyfile',
    'certfile': 'ServerApp.certfile',
    'client-ca': 'ServerApp.client_ca',
    'notebook-dir': 'ServerApp.notebook_dir',
    'browser': 'ServerApp.browser',
    #'gateway-url': 'GatewayClient.url',
})

#-----------------------------------------------------------------------------
# NotebookApp
#-----------------------------------------------------------------------------

from . import shim
from . import traits


class NotebookApp(
    shim.NBClassicConfigShimMixin,
    ExtensionAppJinjaMixin,
    ExtensionApp,
    traits.NotebookAppTraits,
):

    name = 'notebook'
    version = __version__
    description = _("""The Jupyter HTML Notebook.

    This launches a Tornado based HTML Notebook Server that serves up an HTML5/Javascript Notebook client.""")

    aliases = aliases
    flags = flags
    extension_url = "/tree"

    # Override the default open_Browser trait in ExtensionApp,
    # setting it to True.
    open_browser = Bool(
        True,
        help="""Whether to open in a browser after starting.
        The specific browser used is platform dependent and
        determined by the python standard library `webbrowser`
        module, unless it is overridden using the --browser
        (ServerApp.browser) configuration option.
        """
    ).tag(config=True)

    static_custom_path = List(Unicode(),
        help=_("""Path to search for custom.js, css""")
    )

    @default('static_custom_path')
    def _default_static_custom_path(self):
        return [
            os.path.join(d, 'custom') for d in (
                self.config_dir,
                DEFAULT_STATIC_FILES_PATH)
        ]

    extra_nbextensions_path = List(Unicode(), config=True,
        help=_("""extra paths to look for Javascript notebook extensions""")
    )

    @property
    def nbextensions_path(self):
        """The path to look for Javascript notebook extensions"""
        path = self.extra_nbextensions_path + jupyter_path('nbextensions')
        # FIXME: remove IPython nbextensions path after a migration period
        try:
            from IPython.paths import get_ipython_dir
        except ImportError:
            pass
        else:
            path.append(os.path.join(get_ipython_dir(), 'nbextensions'))
        return path

    @property
    def static_paths(self):
        """Rename trait in jupyter_server."""
        return self.static_file_path

    @property
    def template_paths(self):
        """Rename trait for Jupyter Server."""
        return self.template_file_path

    def _prepare_templates(self):
        super(NotebookApp, self)._prepare_templates()

        # Get translations from notebook package.
        base_dir = os.path.dirname(notebook.__file__)

        nbui = gettext.translation('nbui', localedir=os.path.join(base_dir, 'notebook/i18n'), fallback=True)
        self.jinja2_env.install_gettext_translations(nbui, newstyle=False)

    def initialize_settings(self):
        """Add settings to the tornado app."""
        if self.ignore_minified_js:
            self.log.warning(_("""The `ignore_minified_js` flag is deprecated and no longer works."""))
            self.log.warning(_("""Alternatively use `%s` when working on the notebook's Javascript and LESS""") % 'npm run build:watch')
            warnings.warn(_("The `ignore_minified_js` flag is deprecated and will be removed in Notebook 6.0"), DeprecationWarning)

        settings = dict(
            static_custom_path=self.static_custom_path,
            static_handler_args = {
                # don't cache custom.js
                'no_cache_paths': [
                    url_path_join(
                        self.serverapp.base_url,
                        'static',
                        self.name,
                        'custom'
                    )
                ],
            },
            ignore_minified_js=self.ignore_minified_js,
            mathjax_url=self.mathjax_url,
            mathjax_config=self.mathjax_config,
            nbextensions_path=self.nbextensions_path,
        )
        self.settings.update(**settings)

    def initialize_handlers(self):
        """Load the (URL pattern, handler) tuples for each component."""
        # Order matters. The first handler to match the URL will handle the request.
        handlers = []
        # load extra services specified by users before default handlers
        for service in self.settings['extra_services']:
            handlers.extend(load_handlers(service))

        handlers.extend(load_handlers('nbclassic.tree.handlers'))
        handlers.extend(load_handlers('nbclassic.notebook.handlers'))
        handlers.extend(load_handlers('nbclassic.edit.handlers'))

        # Add terminal handlers
        handlers.append(
            (r"/terminals/(\w+)", TerminalHandler)
        )

        handlers.append(
            (r"/nbextensions/(.*)", FileFindHandler, {
                'path': self.settings['nbextensions_path'],
                'no_cache_paths': ['/'], # don't cache anything in nbextensions
            }),
        )
        handlers.append(
            (r"/custom/(.*)", FileFindHandler, {
                'path': self.settings['static_custom_path'],
                'no_cache_paths': ['/'], # don't cache anything in nbextensions
            }),
        )
        # Add new handlers to Jupyter server handlers.
        self.handlers.extend(handlers)

#-----------------------------------------------------------------------------
# Main entry point
#-----------------------------------------------------------------------------

main = launch_new_instance = NotebookApp.launch_instance
