import inspect
import warnings
import textwrap


def shim_message(module, shimmed_module):
    msg = textwrap.dedent("""
    {} has been moved to {}. 
    
    This API will be dropped in the next major
    release of jupyter/notebook. 
    """.format(module, shimmed_module))
    # Strip leading+ending space.
    msg = msg.rstrip().lstrip()
    return msg


def jupyter_server_shim(shim=None):
    """Central warning message for all notebook-->jupyter_server shims"""
    # Get source name of this shim.
    previous_frame = inspect.currentframe().f_back
    module = inspect.getmodule(previous_frame).__name__

    if shim is None:
        shim = module.replace('notebook', 'jupyter_server', 1)

    msg = shim_message(module, shim)
    warnings.warn(msg, DeprecationWarning)