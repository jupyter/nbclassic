import warnings
from .shimwarning import shim_message
from jupyter_core.application import JupyterApp
from traitlets.config.loader import Config

class ConfLoader(JupyterApp):
    def __init__(self, name, argv):
        self.name = name
        self.load_config_file()
        self.parse_command_line(argv)

def load_config(conf_name, argv):
    conf = ConfLoader(conf_name, argv)
    return conf.config

def shim_configs(notebook_config_name: None, server_config_name: None, extension_config_name: None, argv=None):

    notebook_config = load_config(notebook_config_name, argv)
    server_config = load_config(server_config_name, argv)
    extension_config = load_config(extension_config_name, argv)

    _print_warnings(notebook_config, server_config)

    merged_config = Config()
    merged_config.ServerApp = notebook_config.NotebookApp
    merged_config.merge(notebook_config)
    merged_config.merge(server_config)
    merged_config.merge(extension_config)
    return merged_config

def _print_warnings(notebook_config, server_config):
    deprecated = list(notebook_config.NotebookApp.keys())
    if deprecated:
        print("==============================================================================================")
        print("You are using NotebookApp settings that will be deprecated at the next major notebook release.")
        print("Please migrate following settings from NotebookApp to ServerApp:")
        print("  {}".format(deprecated))
        print("Read more on https://jupyter-server.readthedocs.io/en/latest/migrate-from-notebook.html")
        print("==============================================================================================")
        warnings.warn(
            "NotebookApp configuration is deprecated. Migrate them to ServerApp",
            DeprecationWarning, stacklevel=2,
        )
