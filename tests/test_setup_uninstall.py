from collective.casestudy import PACKAGE_NAME

import pytest


@pytest.fixture(autouse=True)
def uninstalled(installer):
    installer.uninstall_product(PACKAGE_NAME)


def test_product_uninstalled(installer):
    """Test if collective.casestudy is cleanly uninstalled."""
    assert installer.is_product_installed(PACKAGE_NAME) is False


def test_browserlayer_removed(browser_layers):
    """Test that ICaseStudyLayer is removed."""
    from collective.casestudy.interfaces import ICaseStudyLayer

    assert ICaseStudyLayer not in browser_layers
