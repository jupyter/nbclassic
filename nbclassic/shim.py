import os
import sys
import re
from functools import wraps
from copy import deepcopy
from traitlets import TraitError, HasTraits
from traitlets.config.application import catch_config_error
from traitlets.config.loader import (
    KVArgParseConfigLoader,
    Config,
)
from jupyter_core.application import JupyterApp
from jupyter_server.serverapp import ServerApp
from .traits import NotebookAppTraits

class NBClassicConfigShimMixin:
    """A Mixin class for shimming configuration from
    NotebookApp to ServerApp. This class handles warnings, errors,
    etc.

    This class should be used during a transition period for apps
    that are switching from depending on NotebookApp to ServerApp.

    After one release cycle, this class can be safely removed
    from the inheriting class.

    TL;DR

    The entry point to shimming is at the `update_config` method.
    Once traits are loaded, before updating config across all
    configurable objects, this class injects a method to reroute
    traits to their *most logical* classes.

    This class raises warnings when:
        1. a trait has moved.
        2. a trait is redundant across classes.

    Redundant traits across multiple classes now must be
    configured separately, *or* removed from their old
    location to avoid this warning.

    For a longer description on how individual traits are handled,
    read the docstring under `shim_config_from_notebook_to_jupyter_server`.
    """
    @wraps(JupyterApp.update_config)
    def update_config(self, config):
        # Shim traits to handle transition from NotebookApp to ServerApp
        shimmed_config = self.shim_config_from_notebook_to_jupyter_server(config)
        super().update_config(shimmed_config)

    def _shim_notebookapp_config(
        self,
        trait_name,
        trait_value,
        nbapp_traits,
        svapp_traits,
        nbapp_config_shim,
        svapp_config_shim
        ):
        """Filter traits in an old notebookapp config to their
        new destinations, i.e. either NotebookApp or ServerApp.

        This method raises warnings when:
        1. a trait has moved.
        2. a trait is redundant across classes.

        Redundant traits across multiple classes now must be
        configured separately, *or* removed from their old
        location to avoid this warning.
        """
        if all((
            trait_name in svapp_traits,
            trait_name in nbapp_traits
        )):
            self.log.warning(
                "This trait is redundant."
            )
            nbapp_config_shim.update({trait_name: trait_value})
        elif trait_name in svapp_traits:
            self.log.warning(
                "'{trait_name}' has moved from NotebookApp to ServerApp. Be sure to update your config before our next release."
                "".format(trait_name=trait_name)
            )
            svapp_config_shim.update({trait_name: trait_value})
        elif trait_name in nbapp_traits:
            nbapp_config_shim.update({trait_name: trait_value})
        else:
            raise TraitError("Trait not found.")

    def shim_config_from_notebook_to_jupyter_server(self, config):
        """Reorganizes a config object to reroute traits to their expected destinations
        after the transition from NotebookApp to ServerApp.

        ---- TL;DR ---------------

        A detailed explanation of how traits are handled:

        1. If the argument is prefixed with `ServerApp`,
            pass this trait to `ServerApp`.
        2. If the argument is prefixed with `NotebookApp`,
            - If the argument is a trait of `NotebookApp` *and* `ServerApp`:
                1. Raise a warning—**for the extension developers**—that
                    there's redundant traits.
                2. Pass trait to `NotebookApp`.
            - If the argument is a trait of just `ServerApp` only
                (i.e. the trait moved from `NotebookApp` to `ServerApp`):
                1. Raise a `"DeprecationWarning: this trait has moved"`
                    **for the user**.
                2. Migrate/write the trait to a new config file if it came
                    from a config file.
                3. Pass trait to `ServerApp`.
            - If the argument is a trait of `NotebookApp` only, pass trait
                to `NotebookApp`.
            - If the argument is not found in any object, raise a
                `"Trait not found."` error.
        3. If the argument is prefixed with `ExtensionApp`:
            - If the argument is a trait of `ExtensionApp` and either
                `NotebookApp` or `ServerApp`,
                1. Raise a warning—**for the extension developers**—that
                    there's redundant traits.
                2. Pass trait to Step 2 above.
            - If the argument is *not* a trait of `ExtensionApp`, but *is*
                a trait of either `NotebookApp` or `ServerApp` (i.e. the trait
                moved from `ExtensionApp` to `NotebookApp`/`ServerApp`):
                1. Raise a `"DeprecationWarning: this trait has moved"`
                    **for the user**.
                2. Migrate/write the trait to a new config file if it came
                    from a config file.
                2. Pass trait to Step 2 above.
            - If the argument is *not* a trait of `ExtensionApp` and not a
                trait of either `NotebookApp` or `ServerApp`, raise a
                `"Trait not found."` error.

        """
        # Pop out the various configurable objects that we need to evaluate.
        nbapp_config = config.pop('NotebookApp', {})
        svapp_config = config.pop('ServerApp', {})
        extapp_config = config.pop(self.__class__.__name__, {})

        # Created shimmed configs.
        # Leave the rest of the config alone.
        config_shim = deepcopy(config)
        svapp_config_shim = Config()
        nbapp_config_shim = Config()
        extapp_config_shim = Config()

        extapp_traits = self.__class__.class_trait_names()
        svapp_traits = ServerApp.class_trait_names()
        nbapp_traits = NotebookAppTraits.class_trait_names()

        # 1. Handle ServerApp traits.
        svapp_config_shim.update(svapp_config)

        # 2. Handle NotebookApp traits.
        for name, value in nbapp_config.items():
            self._shim_notebookapp_config(
                name,
                value,
                nbapp_traits,
                svapp_traits,
                nbapp_config_shim,
                svapp_config_shim
            )

        # 3. Handle ExtensionApp traits.
        for name, value in extapp_config.items():
            if all([
                name in extapp_traits,
                any([name in svapp_traits, name in nbapp_traits])
            ]):
                self.log.warning(
                    "This trait is redundant."
                )
                nbapp_config_shim.update({name: value})
            elif all([
                name not in extapp_traits,
                any([name in svapp_traits, name in nbapp_traits])
            ]):
                self.log.warning(
                    "'{trait_name}' has moved from NotebookApp to ServerApp. Be sure to update your config before our next release."
                    "".format(trait_name=name)
                )
                self._shim_notebookapp_config(
                    name,
                    value,
                    nbapp_traits,
                    svapp_traits,
                    nbapp_config_shim,
                    svapp_config_shim
                )
            elif name is extapp_traits:
                extapp_config_shim.update({name: value})
            else:
                raise TraitError("Trait not found.")

        # Update the shimmed config.
        config_shim.update(
            {
                'NotebookApp': nbapp_config_shim,
                'ServerApp': svapp_config_shim,
                self.__class__.__name__: extapp_config_shim
            }
        )
        return config_shim