import io
import logging
import pytest
from traitlets import default
from nbclassic.notebookapp import NotebookApp

pytest_plugins = ["jupyter_server.pytest_plugin"]


@pytest.fixture
def nbapp_log():
    """An io stream with the NotebookApp's logging output"""
    stream = io.StringIO()
    return stream


@pytest.fixture(autouse=True)
def notebookapp_logcapture(monkeypatch, nbapp_log):
    """"""
    @default('log')
    def _log_default(self):
        """Start logging for this application.
        The default is to log to stderr using a StreamHandler, if no default
        handler already exists.  The log level starts at logging.WARN, but this
        can be adjusted by setting the ``log_level`` attribute.
        """
        log = super(self.__class__, self)._log_default()
        _log_handler = logging.StreamHandler(nbapp_log)
        _log_formatter = self._log_formatter_cls(
            fmt=self.log_format,
            datefmt=self.log_datefmt
        )
        _log_handler.setFormatter(_log_formatter)
        log.addHandler(_log_handler)
        return log

    monkeypatch.setattr(NotebookApp, '_log_default', _log_default)
    return _log_default


@pytest.fixture
def jp_server_config():
    return {
        "ServerApp": {
            "jpserver_extensions": {
                "nbclassic": True
            }
        }
    }
