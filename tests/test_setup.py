from collective.casestudy import PACKAGE_NAME
from plone import api
from Products.CMFPlone.utils import get_installer

import pytest


@pytest.fixture
def installer(portal, http_request):
    return get_installer(portal, http_request)


@pytest.fixture
def uninstalled(installer):
    installer.uninstall_product(PACKAGE_NAME)
    return installer


def test_addon_installed(installer):
    assert installer.is_product_installed(PACKAGE_NAME) is True


def test_browserlayer(integration):
    """Test that ICaseStudyLayer is registered."""
    from collective.casestudy.interfaces import ICaseStudyLayer
    from plone.browserlayer import utils

    assert ICaseStudyLayer in utils.registered_layers()


def test_latest_version(integration):
    """Test latest version of default profile."""
    setup = api.portal.get_tool("portal_setup")
    assert setup.getLastVersionForProfile(f"{PACKAGE_NAME}:default")[0] == "1000"


def test_product_uninstalled(uninstalled):
    """Test if collective.casestudy is cleanly uninstalled."""
    assert uninstalled.is_product_installed(PACKAGE_NAME) is False


def test_browserlayer_removed(uninstalled):
    """Test that ICaseStudyLayer is removed."""
    from collective.casestudy.interfaces import ICaseStudyLayer
    from plone.browserlayer import utils

    assert ICaseStudyLayer not in utils.registered_layers()
