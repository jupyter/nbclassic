import os
import sys
import re
from copy import deepcopy
from traitlets import TraitError, HasTraits
from traitlets.config.application import catch_config_error
from traitlets.config.loader import (
    KVArgParseConfigLoader,
    Config,
)
from jupyter_server.serverapp import ServerApp
from .traits import NotebookAppTraits

class NBClassicConfigShimMixin:
    """A Mixin class for shimming configuration from
    NotebookApp to ServerApp.
    """
    def update_config(self, config):
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
        """Properly shim traits with NotebookApp prefix."""
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
        """Reorganize a config object that might have outdated traits.
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