"""``casestudy_workflow`` on a case study.

A case study runs one workflow, bound to its type, so there is no second
workflow to watch here. What matters is that the standard content permissions
follow the listing states: a case study stays out of sight of anonymous
visitors until it is listed, and the people who may edit it narrow as it moves
from draft to verified.
"""

from . import ACCESS
from . import CASESTUDY_WORKFLOW
from . import MODIFY
from . import roles_for
from . import VIEW
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFCore.indexing import processQueue

import pytest


class TestChain:
    def test_a_case_study_runs_its_own_workflow(self, case_study: DexterityContent):
        wt = api.portal.get_tool("portal_workflow")
        assert wt.getChainFor(case_study) == (CASESTUDY_WORKFLOW,)

    def test_it_starts_in_created(self, case_study):
        assert api.content.get_state(obj=case_study) == "created"

    def test_the_catalog_follows_the_state(self, case_study, as_manager):
        """``review_state`` is this workflow's state, so listings can use it."""
        as_manager(case_study, "list")
        processQueue()
        brain = api.content.find(UID=case_study.UID())[0]
        assert brain.review_state == "listed"
        assert f"{CASESTUDY_WORKFLOW}|listed" in brain.workflow_states


class TestVisibility:
    @pytest.mark.parametrize(
        "transitions,expected",
        [
            ([], False),
            (["review"], False),
            (["list"], True),
            (["verify"], True),
            (["verify", "unverify"], True),
            (["archive"], True),
            (["list", "review"], False),
        ],
    )
    @pytest.mark.parametrize("permission", [ACCESS, VIEW])
    def test_public_reading_follows_the_state(
        self,
        case_study,
        as_manager,
        transitions: list[str],
        expected: bool,
        permission: str,
    ):
        for transition in transitions:
            as_manager(case_study, transition)
        assert ("Anonymous" in roles_for(case_study, permission)) is expected

    @pytest.mark.parametrize("role", ["Owner", "Reader", "Contributor", "Editor"])
    def test_a_draft_is_visible_to_the_people_working_on_it(self, case_study, role):
        """The Sharing tab's roles keep working while the case study is private."""
        assert role in roles_for(case_study, VIEW)


class TestEditing:
    def test_the_owner_edits_a_draft(self, case_study):
        assert "Owner" in roles_for(case_study, MODIFY)

    def test_listing_drops_the_owner(self, case_study, as_manager):
        """`listed` drops the Owner but keeps the Editor."""
        as_manager(case_study, "list")
        roles = roles_for(case_study, MODIFY)
        assert "Owner" not in roles
        assert "Editor" in roles

    def test_verifying_locks_editing_down(self, case_study, as_manager):
        """Approving a case study freezes what was approved."""
        as_manager(case_study, "verify")
        assert roles_for(case_study, MODIFY) == ("Manager", "Site Administrator")

    def test_archiving_locks_editing_down(self, case_study, as_manager):
        as_manager(case_study, "archive")
        assert roles_for(case_study, MODIFY) == ("Manager", "Site Administrator")


class TestTransitions:
    @pytest.fixture
    def available(self):
        """Return a helper listing the transitions a manager could fire."""

        def func(obj: DexterityContent) -> set[str]:
            wt = api.portal.get_tool("portal_workflow")
            with api.env.adopt_roles(["Manager"]):
                return {transition["id"] for transition in wt.getTransitionsFor(obj)}

        return func

    def test_the_initial_state_offers_its_exits(self, case_study, available):
        assert available(case_study) == {"list", "verify", "archive", "review"}

    def test_they_follow_a_transition(self, case_study, as_manager, available):
        as_manager(case_study, "verify")
        assert available(case_study) == {"archive", "review", "unverify"}

    def test_publish_is_gone(self, case_study):
        """The publication workflow's transitions no longer apply."""
        with (
            api.env.adopt_roles(["Manager"]),
            pytest.raises(api.exc.InvalidParameterError),
        ):
            api.content.transition(obj=case_study, transition="publish")


class TestGuards:
    """A guard that never denies is decoration."""

    @pytest.mark.parametrize("transition", ["list", "verify", "archive"])
    def test_a_member_cannot_move_the_listing(self, case_study, transition: str):
        with (
            api.env.adopt_roles(["Member"]),
            pytest.raises(api.exc.InvalidParameterError),
        ):
            api.content.transition(obj=case_study, transition=transition)

    def test_a_reviewer_can_verify(self, case_study):
        """Somebody has to be able to, or the workflow is a dead end."""
        with api.env.adopt_roles(["Reviewer"]):
            api.content.transition(obj=case_study, transition="verify")
        assert api.content.get_state(obj=case_study) == "verified"

    def test_an_owner_can_ask_for_a_review(self, case_study):
        with api.env.adopt_roles(["Owner"]):
            api.content.transition(obj=case_study, transition="review")
        assert api.content.get_state(obj=case_study) == "pending"
