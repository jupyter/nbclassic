import types
import inspect
from functools import wraps
from jupyter_server.services.config import ConfigManager
from traitlets import is_trait
from .traits import NotebookAppTraits


class ClassProxyError(Exception):
    pass


def proxy(obj1, obj2, name, overwrite=False):
    """Redirects a method from object 1 to object 2."""
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


def get_nbserver_extensions(config_dir):
    cm = ConfigManager(read_config_path=[config_dir])
    section = cm.get("jupyter_notebook_config")
    extensions = section.get('NotebookApp', {}).get('nbserver_extensions', {})
    return extensions


def _link_jupyter_server_extension(serverapp):
    # Get the extension manager from the server
    manager = serverapp.extension_manager

    # Hack that patches the enabled extensions list, prioritizing
    # jupyter nbclassic. In the future, it would be much better
    # to incorporate a dependency injection system in the
    # Extension manager that allows extensions to list
    # their dependency tree and sort that way.
    def enabled_extensions(self):
        """Dictionary with extension package names as keys
        and an ExtensionPackage objects as values.
        """
        # Pop out the nbclassic extension to prepend
        # this extension at the front of the sorted server extensions.
        nb = self._enabled_extensions.get("nbclassic")
        # Sort all other extensions alphabetically.
        other_extensions = dict(sorted(self._enabled_extensions.items()))
        # Build a new extensions dictionary, sorted with nbclassic first.
        sorted_extensions = {"nbclassic": nb}
        sorted_extensions.update(**other_extensions)
        return sorted_extensions

    manager.__class__.enabled_extensions = property(enabled_extensions)

    # Look to see if nbclassic is enabled. if so,
    # link the nbclassic extension here to load
    # its config. Then, port its config to the serverapp
    # for backwards compatibility.
    try:
        pkg = manager.enabled_extensions["nbclassic"]
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
    config_dir = serverapp.config_dir
    nbserver_extensions = get_nbserver_extensions(config_dir)

    # Link all extensions found in the old locations for
    # notebook server extensions.
    manager.from_jpserver_extensions(nbserver_extensions)
    for name in nbserver_extensions:
        manager.link_extension(name, serverapp)

    return {}


def _load_jupyter_server_extension(serverapp):
    return
