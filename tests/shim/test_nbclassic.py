import pytest
from nbclassic import shim


@pytest.fixture
def server_config():
    return {
        "ServerApp": {
            "jpserver_extensions": {
                "nbclassic": True,
            }
        }
    }



@pytest.fixture
def nbclassic(serverapp):
    return serverapp.extension_manager.extension_points["nbclassic"].app


def list_test_params(param_input):
    params = []
    for test in param_input:
        name, value = test[0], test[1]
        option = (
            '--NotebookApp.'
            '{name}={value}'
            .format(name=name, value=value)
        )
        params.append([[option], name, value])
    return params


@pytest.mark.parametrize(
    'argv,trait_name,trait_value',
    list_test_params([
        ('jinja_environment_options', {}),
        ('jinja_template_vars', {}),
        ('extra_template_paths', []),
        ('quit_button', True),
    ])
)
def test_NBAPP_AND_SVAPP_SHIM_MSG(
    nbclassic,
    nbapp_log,
    argv,
    trait_name,
    trait_value
):
    log = nbapp_log.getvalue()
    # Verify a shim warning appeared.
    assert shim.NBAPP_AND_SVAPP_SHIM_MSG(trait_name) in log
    # Verify the trait was updated.
    assert getattr(nbclassic, trait_name) == trait_value


@pytest.mark.parametrize(
    'argv,trait_name,trait_value',
    list_test_params([
        ('allow_origin', ''),
        ('allow_origin_pat', ''),
        ('allow_credentials', False),
        # ('allow_root', False)         # This trait is hardcoded by jupyter-server pytest extension.
    ])
)
def test_NBAPP_TO_SVAPP_SHIM_MSG(
    serverapp,
    nbapp_log,
    argv,
    trait_name,
    trait_value
):
    # Expected log message.
    log = nbapp_log.getvalue()
    expected_msg = shim.NBAPP_TO_SVAPP_SHIM_MSG(trait_name)
    # Verify a warning message was raised
    assert expected_msg in log
    # Verify that trait changed.
    assert getattr(serverapp, trait_name) == trait_value


@pytest.mark.parametrize(
    'argv,trait_name,trait_value',
    list_test_params([
        #('ignore_minified_js', True),
        ('enable_mathjax', False),
        ('mathjax_config', 'TEST'),
        ('mathjax_url', 'TEST')
    ])
)
def test_nbclassic_traits_pass_shim(
    nbclassic,
    argv,
    trait_name,
    trait_value
):
    assert getattr(nbclassic, trait_name) == trait_value

