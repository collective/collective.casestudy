from collective.casestudy import PACKAGE_NAME
from plone import api

import pytest


@pytest.fixture
def uninstalled(installer):
    installer.uninstall_product(PACKAGE_NAME)
    return installer


def test_addon_installed(installer):
    assert installer.is_product_installed(PACKAGE_NAME) is True


def test_browserlayer(browser_layers):
    """Test that ICaseStudyLayer is registered."""
    from collective.casestudy.interfaces import ICaseStudyLayer

    assert ICaseStudyLayer in browser_layers


def test_latest_version(integration):
    """Test latest version of default profile."""
    setup = api.portal.get_tool("portal_setup")
    assert setup.getLastVersionForProfile(f"{PACKAGE_NAME}:default")[0] == "1000"


def test_product_uninstalled(uninstalled):
    """Test if collective.casestudy is cleanly uninstalled."""
    assert uninstalled.is_product_installed(PACKAGE_NAME) is False


def test_browserlayer_removed(uninstalled, browser_layers):
    """Test that ICaseStudyLayer is removed."""
    from collective.casestudy.interfaces import ICaseStudyLayer

    assert ICaseStudyLayer not in browser_layers
