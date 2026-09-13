"""Upgrade to profile version 2300: install `collective.multiworkflow`.

Adding a dependency to ``metadata.xml`` only reaches *fresh* installs --
GenericSetup reads the dependency list when the profile is first applied and
never again. An existing site needs an upgrade step that installs it, or the
``plone:additionalworkflows`` chain adapter is registered against a package
whose profile was never run, and the provider workflow never appears.
"""

from collective.casestudy import PACKAGE_NAME
from Products.GenericSetup.tool import SetupTool

import pytest


PROFILE_ID = f"{PACKAGE_NAME}:default"
DEPENDENCY_PROFILE = "collective.multiworkflow:default"


@pytest.fixture(scope="class")
def portal(portal_class):
    yield portal_class


@pytest.fixture
def upgrade_step(setup_tool: SetupTool):
    """The single registered step taking 2200 to 2300."""
    steps = [
        step
        for step in setup_tool.listUpgrades(PROFILE_ID, show_old=True, simple=True)
        if step.source == ("2200",) and step.dest == ("2300",)
    ]
    assert len(steps) == 1, f"expected exactly one 2200->2300 step, got {len(steps)}"
    return steps[0]


class TestUpgradeStepRegistered:
    def test_step_exists(self, upgrade_step):
        assert upgrade_step is not None

    def test_it_imports_the_dependency_profile(self, upgrade_step):
        """The step is what installs the package on an existing site."""
        assert upgrade_step.import_profile == f"profile-{DEPENDENCY_PROFILE}"

    def test_it_names_no_import_steps(self, upgrade_step):
        """``import_steps`` splits on whitespace, so a stray value raises.

        A comma-separated list here registers one bogus step id and running
        the upgrade fails with ``ValueError``.
        """
        assert list(upgrade_step.import_steps) == []

    def test_destination_is_not_past_the_profile_version(self, setup_tool: SetupTool):
        """A step whose destination outruns ``metadata.xml`` never shows up."""
        version = setup_tool.getVersionForProfile(PROFILE_ID)
        assert int(version) >= 2300


class TestDependencyInstalled:
    """A fresh install gets the dependency through ``metadata.xml``."""

    def test_dependency_profile_is_applied(self, setup_tool: SetupTool):
        version = setup_tool.getLastVersionForProfile(DEPENDENCY_PROFILE)
        assert version != "unknown"

    def test_chain_adapter_is_usable(self, portal):
        """The proof the profile ran: the workflow it needs is in the tool."""
        from collective.casestudy.subscribers.organization import WORKFLOW_ID
        from plone import api

        wt = api.portal.get_tool("portal_workflow")
        assert wt.getWorkflowById(WORKFLOW_ID) is not None
