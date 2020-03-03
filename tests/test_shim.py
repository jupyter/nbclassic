import pytest
from nbclassic import shim


@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('default_url', '/tree'),
        ('jinja_environment_options', {}),
        ('jinja_template_vars', {}),
        ('extra_template_paths', []),
        ('quit_button', True),
    ]
)
def test_NBAPP_AND_SVAPP_SHIM_MSG(
    nbclassic_entrypoint,
    nbapp_log,
    trait_name,
    trait_value
    ):
    # trait_name = 'max_body_size'
    # trait_value = 10
    arg = '--NotebookApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = nbclassic_entrypoint(arg)
    log = nbapp_log.getvalue()
    # Verify a shim warning appeared.
    assert shim.NBAPP_AND_SVAPP_SHIM_MSG(trait_name) in log
    # Verify the trait was updated.
    assert getattr(app, trait_name) == trait_value


@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        ('allow_origin', ''),
        ('allow_origin_pat', ''),
        ('allow_credentials', False),
        # ('allow_root', False)         # This trait is hardcoded by jupyter-server pytest extension.
    ]
)
def test_NBAPP_TO_SVAPP_SHIM_MSG(
    nbclassic_entrypoint,
    nbapp_log,
    trait_name,
    trait_value
    ):
    # trait_name = 'max_body_size'
    # trait_value = 10
    arg = '--NotebookApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = nbclassic_entrypoint(arg)
    svapp = app.serverapp
    # Expected log message.
    log = nbapp_log.getvalue()
    expected_msg = shim.NBAPP_TO_SVAPP_SHIM_MSG(trait_name)
    # Verify a warning message was raised
    assert expected_msg in log
    # Verify that trait changed.
    assert getattr(svapp, trait_name) == trait_value


@pytest.mark.parametrize(
    'trait_name,trait_value',
    [
        #('ignore_minified_js', True),
        ('enable_mathjax', False),
        ('mathjax_config', 'TEST'),
        ('mathjax_url', 'TEST')
    ]
)
def test_nbclassic_traits_pass_shim(
    nbclassic_entrypoint,
    trait_name,
    trait_value
    ):
    # trait_name = 'max_body_size'
    # trait_value = 10
    arg = '--NotebookApp.{trait_name}={trait_value}'.format(
        trait_name=trait_name,
        trait_value=trait_value
    )
    app = nbclassic_entrypoint(arg)
    assert getattr(app, trait_name) == trait_value

