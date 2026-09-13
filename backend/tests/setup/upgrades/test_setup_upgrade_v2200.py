"""The 2100 -> 2200 upgrade: the Provider content type is removed.

The step is deliberately conditional -- deleting an FTI a site still has
content for leaves objects nothing can render -- so both branches are
asserted here.
"""

from collective.casestudy import PACKAGE_NAME
from collective.casestudy.upgrades.v2200.provider import ADD_PERMISSION
from collective.casestudy.upgrades.v2200.provider import PORTAL_TYPE
from collective.casestudy.upgrades.v2200.provider import provider_content
from collective.casestudy.upgrades.v2200.provider import remove_provider_type
from collective.casestudy.upgrades.v2200.provider import WORKFLOW_ID
from plone import api
from plone.dexterity.fti import DexterityFTI

import pytest


@pytest.fixture
def tools(portal):
    return (
        api.portal.get_tool("portal_types"),
        api.portal.get_tool("portal_workflow"),
    )


@pytest.fixture
def legacy_provider_type(portal, tools):
    """Put the Provider FTI back, as a site upgrading from 2100 still has it."""
    portal_types, _ = tools
    if PORTAL_TYPE not in portal_types:
        fti = DexterityFTI(PORTAL_TYPE)
        fti.klass = "plone.dexterity.content.Container"
        fti.factory = PORTAL_TYPE
        fti.global_allow = True
        portal_types._setObject(PORTAL_TYPE, fti)
    return portal_types[PORTAL_TYPE]


class TestRemoveProviderType:
    def test_removes_the_type(self, legacy_provider_type, tools):
        portal_types, _ = tools
        assert PORTAL_TYPE in portal_types

        remove_provider_type(None)

        assert PORTAL_TYPE not in portal_types

    def test_is_a_no_op_when_the_type_is_already_gone(self, portal, tools):
        """Re-running it, or running it on a fresh 2200 install."""
        portal_types, _ = tools
        remove_provider_type(None)
        remove_provider_type(None)
        assert PORTAL_TYPE not in portal_types

    def test_unbinds_the_workflow(self, legacy_provider_type, tools):
        _, workflow_tool = tools
        workflow_tool.setChainForPortalTypes(
            [PORTAL_TYPE], ("simple_publication_workflow",)
        )
        remove_provider_type(None)
        assert not workflow_tool.getChainForPortalType(PORTAL_TYPE)

    def test_leaves_the_other_types_alone(self, legacy_provider_type, tools):
        portal_types, _ = tools
        remove_provider_type(None)
        assert "CaseStudy" in portal_types
        assert "Organization" in portal_types

    def test_the_default_profile_no_longer_ships_it(self, portal, tools):
        """A fresh install never had the type in the first place."""
        portal_types, _ = tools
        assert PORTAL_TYPE not in portal_types


class TestRefusesWhileContentExists:
    """Migrating Provider content is a manual, editorial step."""

    @pytest.fixture
    def provider_item(self, portal, legacy_provider_type):
        with api.env.adopt_roles(["Manager"]):
            return api.content.create(
                container=portal, type=PORTAL_TYPE, id="legacy-provider"
            )

    def test_finds_the_content(self, provider_item):
        assert len(provider_content()) == 1

    def test_keeps_the_type(self, provider_item, tools):
        portal_types, _ = tools
        remove_provider_type(None)
        assert PORTAL_TYPE in portal_types

    def test_keeps_the_content_usable(self, provider_item, portal):
        remove_provider_type(None)
        assert "legacy-provider" in portal

    def test_says_why(self, provider_item, caplog):
        """A silent no-op would read as a completed upgrade."""
        with caplog.at_level("WARNING", logger=PACKAGE_NAME):
            remove_provider_type(None)
        assert "Migrate them to Organization" in caplog.text
        assert "legacy-provider" in caplog.text

    def test_removes_it_once_the_content_is_gone(self, provider_item, portal, tools):
        """Running the step again after migrating finishes the job."""
        portal_types, _ = tools
        remove_provider_type(None)
        assert PORTAL_TYPE in portal_types

        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=provider_item, check_linkintegrity=False)
        remove_provider_type(None)
        assert PORTAL_TYPE not in portal_types


def test_add_permission_name():
    """Guard the string the rolemap used to carry."""
    assert ADD_PERMISSION == "collective.casestudy: Add Provider"


def test_workflow_id():
    assert WORKFLOW_ID == "provider_workflow"
