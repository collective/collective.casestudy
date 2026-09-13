"""Upgrade to profile version 2400: case studies move to ``casestudy_workflow``.

The ``workflow`` import step binds the type to the new workflow, but a binding
says nothing about the objects: an existing case study has a status only in
``simple_publication_workflow``, and DCWorkflow answers a missing status with
the new workflow's initial state. Without the migration handler every
published case study would silently read as ``created`` -- and, once its role
mappings were rewritten, disappear from the site.
"""

from ...workflow import roles_for
from collections.abc import Callable
from collective.casestudy import PACKAGE_NAME
from collective.casestudy.upgrades.v2400.workflow import migrate_case_studies
from collective.casestudy.upgrades.v2400.workflow import OLD_WORKFLOW_ID
from collective.casestudy.upgrades.v2400.workflow import WORKFLOW_ID
from copy import deepcopy
from DateTime import DateTime
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFCore.indexing import processQueue
from Products.GenericSetup.tool import SetupTool

import pytest


PROFILE_ID = f"{PACKAGE_NAME}:default"


@pytest.fixture
def upgrade_steps(setup_tool: SetupTool) -> list:
    """The steps registered to take the profile from 2300 to 2400."""
    return [
        step
        for step in setup_tool.listUpgrades(PROFILE_ID, show_old=True, simple=True)
        if step.source == ("2300",) and step.dest == ("2400",)
    ]


class TestUpgradeStepRegistered:
    def test_two_steps(self, upgrade_steps):
        assert len(upgrade_steps) == 2

    def test_it_imports_the_workflow_step(self, upgrade_steps):
        """The import step defines the workflow and binds it to the type."""
        import_steps = {
            step_id
            for step in upgrade_steps
            for step_id in getattr(step, "import_steps", ())
        }
        assert import_steps == {"workflow"}

    def test_it_runs_the_migration_handler(self, upgrade_steps):
        handlers = [getattr(step, "handler", None) for step in upgrade_steps]
        assert migrate_case_studies in handlers

    def test_the_workflow_is_imported_before_the_migration(self, upgrade_steps):
        """The handler needs the new workflow to exist."""
        kinds = [
            "import" if getattr(step, "import_steps", ()) else "handler"
            for step in upgrade_steps
        ]
        assert kinds == ["import", "handler"]

    def test_destination_is_not_past_the_profile_version(self, setup_tool: SetupTool):
        """A step whose destination outruns ``metadata.xml`` never shows up."""
        assert int(setup_tool.getVersionForProfile(PROFILE_ID)) >= 2400


@pytest.fixture
def legacy_case_study(
    portal, case_studies_payload
) -> Callable[[str | None], DexterityContent]:
    """Return a helper creating a case study as a site before 2400 holds it.

    The case study is created normally, then stripped of its status in the new
    workflow and given one in ``simple_publication_workflow`` instead, with
    that workflow's role mappings applied.

    :returns: Callable taking the old state -- or ``None`` for a case study
        that never had one -- and returning the case study.
    """
    wt = api.portal.get_tool("portal_workflow")
    old_workflow = wt.getWorkflowById(OLD_WORKFLOW_ID)

    def func(old_state: str | None) -> DexterityContent:
        payload = deepcopy(case_studies_payload[0])
        payload["id"] = f"legacy-{old_state}"
        with api.env.adopt_roles(["Manager"]):
            obj = api.content.create(container=portal, **payload)
        del obj.workflow_history[WORKFLOW_ID]
        if old_state is not None:
            wt.setStatusOf(
                OLD_WORKFLOW_ID,
                obj,
                {
                    "action": None,
                    "actor": "admin",
                    "comments": "",
                    "review_state": old_state,
                    "time": DateTime(),
                },
            )
            if old_state in old_workflow.states:
                old_workflow.updateRoleMappingsFor(obj)
        obj.reindexObject()
        return obj

    return func


class TestMigrateCaseStudies:
    @pytest.mark.parametrize(
        "old_state,expected",
        [
            ("private", "created"),
            ("pending", "pending"),
            ("published", "listed"),
        ],
    )
    def test_state_is_mapped(self, legacy_case_study, old_state: str, expected: str):
        obj = legacy_case_study(old_state)
        migrate_case_studies(None)
        assert api.content.get_state(obj=obj) == expected

    @pytest.mark.parametrize("old_state", [None, "external"])
    def test_anything_else_lands_in_created(self, legacy_case_study, old_state):
        obj = legacy_case_study(old_state)
        migrate_case_studies(None)
        assert api.content.get_state(obj=obj) == "created"

    def test_a_published_case_study_stays_public(self, legacy_case_study):
        obj = legacy_case_study("published")
        migrate_case_studies(None)
        assert "Anonymous" in roles_for(obj, "View")

    def test_a_private_case_study_stays_private(self, legacy_case_study):
        obj = legacy_case_study("private")
        migrate_case_studies(None)
        assert "Anonymous" not in roles_for(obj, "View")

    def test_the_catalog_follows(self, legacy_case_study):
        obj = legacy_case_study("published")
        migrate_case_studies(None)
        processQueue()
        brain = api.content.find(UID=obj.UID(), unrestricted=True)[0]
        assert brain.review_state == "listed"
        assert f"{WORKFLOW_ID}|listed" in brain.workflow_states

    def test_the_history_says_where_the_state_came_from(self, legacy_case_study):
        obj = legacy_case_study("published")
        migrate_case_studies(None)
        wt = api.portal.get_tool("portal_workflow")
        status = wt.getStatusOf(WORKFLOW_ID, obj)
        assert f"{OLD_WORKFLOW_ID} (published)" in status["comments"]

    def test_it_is_idempotent(self, legacy_case_study):
        obj = legacy_case_study("published")
        migrate_case_studies(None)
        migrate_case_studies(None)
        assert len(obj.workflow_history[WORKFLOW_ID]) == 1

    def test_a_case_study_already_on_the_new_workflow_is_left_alone(
        self, portal, case_studies_payload
    ):
        """Content created after the import step already has a real state."""
        with api.env.adopt_roles(["Manager"]):
            obj = api.content.create(container=portal, **case_studies_payload[1])
            api.content.transition(obj=obj, transition="verify")
        history = len(obj.workflow_history[WORKFLOW_ID])

        migrate_case_studies(None)

        assert api.content.get_state(obj=obj) == "verified"
        assert len(obj.workflow_history[WORKFLOW_ID]) == history

    def test_other_types_are_untouched(self, portal, organizations_payload):
        with api.env.adopt_roles(["Manager"]):
            organization = api.content.create(
                container=portal, **organizations_payload[0]
            )
        migrate_case_studies(None)
        wt = api.portal.get_tool("portal_workflow")
        assert wt.getStatusOf(WORKFLOW_ID, organization) is None
