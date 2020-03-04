
import io
import logging
import pytest
from traitlets import (
    Unicode,
    Bool,
    Dict,
    default
)
from jupyter_server.extension.application import ExtensionApp

from nbclassic.notebookapp import NotebookApp
from nbclassic import shim


class MockExtensionApp(
    shim.NBClassicConfigShimMixin,
    ExtensionApp
    ):
    """Mock an extension app that previously inherited NotebookApp."""
    extension_name = 'mockext'

    # ------ Traits found ServerApp, NotebookApp, and MockExtensionApp

    default_url = Unicode(config=True)

    # ------ Traits found Notebook and MockExtensionApp

    enable_mathjax = Bool(config=True)

    # ------ Traits found ServerApp and MockExtensionApp

    allow_origin = Unicode(config=True)
    allow_origin_pat = Unicode(config=True)




@pytest.fixture
def extapp_log():
    """An io stream with the NotebookApp's logging output"""
    stream = io.StringIO()
    return stream


@pytest.fixture(autouse=True)
def extapp_logcapture(monkeypatch, extapp_log):
    """"""
    @default('log')
    def _log_default(self):
        """Start logging for this application.
        The default is to log to stderr using a StreamHandler, if no default
        handler already exists.  The log level starts at logging.WARN, but this
        can be adjusted by setting the ``log_level`` attribute.
        """
        log = super(self.__class__, self)._log_default()
        _log_handler = logging.StreamHandler(extapp_log)
        _log_formatter = self._log_formatter_cls(
            fmt=self.log_format,
            datefmt=self.log_datefmt
        )
        _log_handler.setFormatter(_log_formatter)
        log.addHandler(_log_handler)
        return log

    monkeypatch.setattr(MockExtensionApp, '_log_default', _log_default)
    return _log_default



@pytest.fixture
def extapp_entrypoint(configurable_serverapp):
    """A fixture that mimics the nbclassic command-line entrypoint.
    You can pass a string or list of args that look like
    the args from the CLI.

    Example:
    > jupyter nbclassic --ServerApp.port=8889
    becomes
    nbclassic_entrypoint('--ServerApp.port=8889')
    """
    def built_entrypoint(argv):
        if isinstance(argv, str):
            argv = [argv]
        svapp = configurable_serverapp(argv=argv)

        # Append Nbclassic
        nbapp = NotebookApp(parent=svapp)
        nbapp.initialize(svapp)

        # Append extapp
        extapp = MockExtensionApp(parent=svapp)
        extapp.initialize(svapp)
        return extapp

    yield built_entrypoint



@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('default_url', '/tree'),
    ]
)
def test_EXTAPP_AND_NBAPP_AND_SVAPP_SHIM_MSG(
    extapp_entrypoint,
    extapp_log,
    trait_name,
    trait_value
    ):
    arg = '--MockExtensionApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = extapp_entrypoint(arg)
    log = extapp_log.getvalue()
    # Verify a shim warning appeared.
    log_msg = shim.EXTAPP_AND_NBAPP_AND_SVAPP_SHIM_MSG(trait_name, 'MockExtensionApp')
    assert log_msg in log
    # Verify the trait was updated.
    assert getattr(app, trait_name) == trait_value



@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('enable_mathjax', False)
    ]
)
def test_EXTAPP_AND_NBAPP_SHIM_MSG(
    extapp_entrypoint,
    extapp_log,
    trait_name,
    trait_value
    ):
    arg = '--MockExtensionApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = extapp_entrypoint(arg)
    log = extapp_log.getvalue()
    # Verify a shim warning appeared.
    log_msg = shim.EXTAPP_AND_NBAPP_SHIM_MSG(trait_name, 'MockExtensionApp')
    assert log_msg in log
    # Verify the trait was updated.
    assert getattr(app, trait_name) == trait_value


@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('allow_origin', ''),
        ('allow_origin_pat', ''),
    ]
)
def test_EXTAPP_AND_SVAPP_SHIM_MSG(
    extapp_entrypoint,
    extapp_log,
    trait_name,
    trait_value
    ):
    arg = '--MockExtensionApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = extapp_entrypoint(arg)
    log = extapp_log.getvalue()
    # Verify a shim warning appeared.
    log_msg = shim.EXTAPP_AND_SVAPP_SHIM_MSG(trait_name, 'MockExtensionApp')
    assert log_msg in log
    # Verify the trait was updated.
    assert getattr(app, trait_name) == trait_value


@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('jinja_environment_options', {}),
        ('jinja_template_vars', {}),
        ('extra_template_paths', []),
        ('quit_button', True),
    ]
)
def test_NOT_EXTAPP_NBAPP_AND_SVAPP_SHIM_MSG(
    extapp_entrypoint,
    extapp_log,
    trait_name,
    trait_value
    ):
    arg = '--MockExtensionApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = extapp_entrypoint(arg)
    log = extapp_log.getvalue()
    # Verify a shim warning appeared.
    log_msg = shim.NOT_EXTAPP_NBAPP_AND_SVAPP_SHIM_MSG(trait_name, 'MockExtensionApp')
    assert log_msg in log
    # Verify the trait was updated.
    assert getattr(app.serverapp, trait_name) == trait_value



@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('allow_credentials', False),
    ]
)
def test_EXTAPP_TO_SVAPP_SHIM_MSG(
    extapp_entrypoint,
    extapp_log,
    trait_name,
    trait_value
    ):
    arg = '--MockExtensionApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = extapp_entrypoint(arg)
    log = extapp_log.getvalue()
    # Verify a shim warning appeared.
    log_msg = shim.EXTAPP_TO_SVAPP_SHIM_MSG(trait_name, 'MockExtensionApp')
    assert log_msg in log
    # Verify the trait was updated.
    assert getattr(app.serverapp, trait_name) == trait_value



@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('mathjax_config', 'TEST'),
        ('mathjax_url', 'TEST')
    ]
)
def test_EXTAPP_TO_NBAPP_SHIM_MSG(
    extapp_entrypoint,
    extapp_log,
    trait_name,
    trait_value
    ):
    arg = '--MockExtensionApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = extapp_entrypoint(arg)
    log = extapp_log.getvalue()
    # Verify a shim warning appeared.
    log_msg = shim.EXTAPP_TO_NBAPP_SHIM_MSG(trait_name, 'MockExtensionApp')
    assert log_msg in log
