"""Upgrade to profile version 2600: the querystring field labels.

The Facet field used the Services msgids, and the Provider Services field
shared ``label_services`` with the Services behavior field. The registry stores
the msgids themselves, so an existing site keeps the old ones -- and keeps
showing the wrong text -- until the ``plone.app.registry`` step runs again.
"""

from collective.casestudy import PACKAGE_NAME
from plone import api
from Products.GenericSetup.tool import SetupTool

import pytest


PROFILE_ID = f"{PACKAGE_NAME}:default"


@pytest.fixture
def upgrade_steps(setup_tool: SetupTool) -> list:
    """The steps registered to take the profile from 2500 to 2600."""
    return [
        step
        for step in setup_tool.listUpgrades(PROFILE_ID, show_old=True, simple=True)
        if step.source == ("2500",) and step.dest == ("2600",)
    ]


class TestUpgradeStepRegistered:
    def test_one_step(self, upgrade_steps):
        assert len(upgrade_steps) == 1

    def test_it_imports_the_registry(self, upgrade_steps):
        assert list(upgrade_steps[0].import_steps) == ["plone.app.registry"]

    def test_destination_is_the_profile_version(self, setup_tool: SetupTool):
        """A step whose destination outruns ``metadata.xml`` never shows up."""
        assert int(setup_tool.getVersionForProfile(PROFILE_ID)) >= 2600


class TestRunningTheUpgrade:
    """Run the step against a registry as a 2500 site holds it."""

    @pytest.mark.parametrize(
        "record,old,new",
        [
            (
                "plone.app.querystring.field.facets.title",
                "label_services",
                "label_facets",
            ),
            (
                "plone.app.querystring.field.facets.description",
                "description_qs_services",
                "description_qs_facets",
            ),
            (
                "plone.app.querystring.field.services.title",
                "label_services",
                "label_provider_services",
            ),
        ],
    )
    def test_it_replaces_the_msgid(
        self, upgrade_steps, setup_tool: SetupTool, record: str, old: str, new: str
    ):
        api.portal.set_registry_record(record, old)

        upgrade_steps[0].doStep(setup_tool)

        assert api.portal.get_registry_record(record) == new
