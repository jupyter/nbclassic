"""
This module contains a Jupyter Server extension that attempts to
make classic server and notebook extensions work in the new server.

Unfortunately, you'll notice that requires some major monkey-patching.
The goal is that this extension will only be used as a temporary
patch to transition extension authors from classic notebook server to jupyter_server.
"""
import os
import types
import inspect
from functools import wraps
from jupyter_core.paths import jupyter_config_path
from traitlets.traitlets import is_trait

import notebook

import jupyter_server
from jupyter_server.services.config.manager import ConfigManager
from .traits import NotebookAppTraits


class ClassProxyError(Exception):
    pass


def proxy(obj1, obj2, name, overwrite=False):
    """Redirects a method, property, or trait from object 1 to object 2."""
    if hasattr(obj1, name) and overwrite is False:
        raise ClassProxyError(
            "Cannot proxy the attribute '{name}' from {cls2} because "
            "{cls1} already has this attribute.".format(
                name=name,
                cls1=obj1.__class__,
                cls2=obj2.__class__
            )
        )
    attr = getattr(obj2, name)

    # First check if this thing is a trait (see traitlets)
    cls_attr = getattr(obj2.__class__, name)
    if is_trait(cls_attr) or type(attr) == property:
        thing = property(lambda self: getattr(obj2, name))

    elif isinstance(attr, types.MethodType):
        @wraps(attr)
        def thing(self, *args, **kwargs):
            return attr(*args, **kwargs)

    # Anything else appended on the class is just an attribute of the class.
    else:
        thing = attr

    setattr(obj1.__class__, name, thing)


def public_members(obj):
    members = inspect.getmembers(obj)
    return [m for m, _ in members if not m.startswith('_')]


def diff_members(obj1, obj2):
    """Return all attribute names found in obj2 but not obj1"""
    m1 = public_members(obj1)
    m2 = public_members(obj2)
    return set(m2).difference(m1)


def get_nbserver_extensions(config_dirs):
    cm = ConfigManager(read_config_path=config_dirs)
    section = cm.get("jupyter_notebook_config")
    extensions = section.get('NotebookApp', {}).get('nbserver_extensions', {})
    return extensions


def _link_jupyter_server_extension(serverapp):
    # Get the extension manager from the server
    manager = serverapp.extension_manager
    logger = serverapp.log

    # Hack that patches the enabled extensions list, prioritizing
    # jupyter nbclassic. In the future, it would be much better
    # to incorporate a dependency injection system in the
    # Extension manager that allows extensions to list
    # their dependency tree and sort that way.
    def sorted_extensions(self):
        """Dictionary with extension package names as keys
        and an ExtensionPackage objects as values.
        """
        # Sort the keys and
        keys = sorted(self.extensions.keys())
        keys.remove("nbclassic")
        keys = ["nbclassic"] + keys
        return {key: self.extensions[key] for key in keys}

    manager.__class__.sorted_extensions = property(sorted_extensions)

    # Look to see if nbclassic is enabled. if so,
    # link the nbclassic extension here to load
    # its config. Then, port its config to the serverapp
    # for backwards compatibility.
    try:
        pkg = manager.extensions["nbclassic"]
        pkg.link_point("jupyter-nbclassic", serverapp)
        point = pkg.extension_points["jupyter-nbclassic"]
        nbapp = point.app
    except Exception:
        nbapp = NotebookAppTraits()

    # Proxy NotebookApp traits through serverapp to notebookapp.
    members = diff_members(serverapp, nbapp)
    for m in members:
        proxy(serverapp, nbapp, m)

    # Find jupyter server extensions listed as notebook server extensions.
    jupyter_paths = jupyter_config_path()
    config_dirs = jupyter_paths + [serverapp.config_dir]
    nbserver_extensions = get_nbserver_extensions(config_dirs)

    # Link all extensions found in the old locations for
    # notebook server extensions.
    for name, enabled in nbserver_extensions.items():
        # If the extension is already enabled in the manager, i.e.
        # because it was discovered already by Jupyter Server
        # through its jupyter_server_config, then don't re-enable here.
        if name not in manager.extensions:
            successful = manager.add_extension(name, enabled=enabled)
            if successful:
                logger.info(
                    "{name} | extension was found and enabled by nbclassic. "
                    "Consider moving the extension to Jupyter Server's "
                    "extension paths.".format(name=name)
                )
                manager.link_extension(name)

    # Monkeypatch the IPython handler to pull templates from the "correct"
    # Jinja Environment, namespaced by "notebook".
    def get_template(self, name):
        """Return the jinja template object for a given name"""
        return self.settings['notebook_jinja2_env'].get_template(name)

    notebook.base.handlers.IPythonHandler.get_template = get_template


    # Monkey-patch Jupyter Server's and nbclassic's static path list to include
    # the classic notebooks static folder.

    def static_file_path_jupyter_server(self):
        """return extra paths + the default location"""
        return self.extra_static_paths + [jupyter_server.DEFAULT_STATIC_FILES_PATH, notebook.DEFAULT_STATIC_FILES_PATH]

    serverapp.__class__.static_file_path = property(
        static_file_path_jupyter_server)

    def static_file_path_nbclassic(self):
        """return extra paths + the default location"""
        # NBExtensions look for classic notebook static files under the `/static/notebook/...`
        # URL. Unfortunately, this conflicts with nbclassic's new static endpoints which are
        # prefixed with `/static/notebooks`, and therefore, serves these files under
        # `/static/notebook/notebooks/...`. This monkey-patch places a new file-finder path
        # to nbclassic's static file handlers that drops the extra "notebook".
        return self.extra_static_paths + \
            [os.path.join(notebook.DEFAULT_STATIC_FILES_PATH,
                          "notebook"), notebook.DEFAULT_STATIC_FILES_PATH]

    nbapp.__class__.static_file_path = property(static_file_path_nbclassic)


def _load_jupyter_server_extension(serverapp):
    # Patch the config service manager to find the
    # proper path for old notebook frontend extensions
    config_manager = serverapp.config_manager
    read_config_path = config_manager.read_config_path
    read_config_path += [os.path.join(p, 'nbconfig')
                         for p in jupyter_config_path()]
    config_manager.read_config_path = read_config_path
