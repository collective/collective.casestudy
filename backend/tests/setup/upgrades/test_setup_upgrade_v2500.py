"""Upgrade to profile version 2500: the listing and verification querystring fields.

Querystring fields live in ``registry/*.xml``, which GenericSetup reads on
install only. An existing site gets the four new Yes/No fields -- and the new
groups of the fields it already has -- only through an upgrade step that
re-runs the ``plone.app.registry`` import step.
"""

from collective.casestudy import PACKAGE_NAME
from plone import api
from plone.registry.interfaces import IRegistry
from Products.GenericSetup.tool import SetupTool
from zope.component import getUtility

import pytest


PROFILE_ID = f"{PACKAGE_NAME}:default"

#: Prefix of the records of one of the fields the upgrade adds.
NEW_FIELD = "plone.app.querystring.field.provider_verified"

#: Record whose value the upgrade changes on an existing site.
REGROUPED_FIELD = "plone.app.querystring.field.usages.group"


@pytest.fixture
def upgrade_steps(setup_tool: SetupTool) -> list:
    """The steps registered to take the profile from 2400 to 2500."""
    return [
        step
        for step in setup_tool.listUpgrades(PROFILE_ID, show_old=True, simple=True)
        if step.source == ("2400",) and step.dest == ("2500",)
    ]


class TestUpgradeStepRegistered:
    def test_one_step(self, upgrade_steps):
        assert len(upgrade_steps) == 1

    def test_it_imports_the_registry(self, upgrade_steps):
        assert list(upgrade_steps[0].import_steps) == ["plone.app.registry"]

    def test_destination_is_the_profile_version(self, setup_tool: SetupTool):
        """A step whose destination outruns ``metadata.xml`` never shows up."""
        assert setup_tool.getVersionForProfile(PROFILE_ID) == "2500"


class TestRunningTheUpgrade:
    """Run the step against a registry as a 2400 site holds it."""

    def test_it_adds_a_missing_field(self, upgrade_steps, setup_tool: SetupTool):
        registry = getUtility(IRegistry)
        # Copied before deleting: the records are removed while iterating.
        names = list(registry.records.keys())
        for name in [name for name in names if name.startswith(NEW_FIELD)]:
            del registry.records[name]
        assert f"{NEW_FIELD}.title" not in registry.records

        upgrade_steps[0].doStep(setup_tool)

        assert f"{NEW_FIELD}.title" in registry.records

    def test_it_regroups_an_existing_field(self, upgrade_steps, setup_tool: SetupTool):
        api.portal.set_registry_record(REGROUPED_FIELD, "Case Study")

        upgrade_steps[0].doStep(setup_tool)

        assert api.portal.get_registry_record(REGROUPED_FIELD) == "Case Studies"
