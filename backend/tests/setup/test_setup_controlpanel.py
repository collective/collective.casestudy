"""The Case Study control panel entry.

The configlet is what makes the panel reachable: the classic UI lists it, and
plone.restapi's ``@controlpanels`` serializes it for the frontend.
"""

from plone import api

import pytest


CONFIGLET_ID = "case_study"


@pytest.fixture
def configlet(portal):
    """Return the Case Study configlet, or None when it is not installed."""
    tool = api.portal.get_tool("portal_controlpanel")
    for action in tool.listActions():
        if action.getId() == CONFIGLET_ID:
            return action
    return None


class TestControlPanelConfiglet:
    def test_installed(self, configlet):
        assert configlet is not None

    def test_title(self, configlet):
        assert configlet.title == "Case Study Settings"

    def test_category(self, configlet):
        assert configlet.category == "Products"

    def test_permission(self, configlet):
        assert configlet.permissions == ("Manage portal",)

    def test_has_an_icon(self, configlet):
        """Without one the panel is the only unlabelled tile in the listing."""
        assert configlet.getIconExpression()

    def test_icon_is_a_bootstrap_icon_name(self, configlet):
        """Plone 6 resolves the expression against its Bootstrap icon set."""
        assert configlet.getIconExpression() == "string:briefcase"

    def test_icon_name_exists_in_the_icon_set(self):
        """A name the set does not carry renders nothing at all."""
        from pathlib import Path

        import plone.staticresources

        icons = Path(plone.staticresources.__file__).parent / ("static/icons-bootstrap")
        assert (icons / "briefcase.svg").exists()
