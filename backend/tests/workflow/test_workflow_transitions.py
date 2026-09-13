"""Transitions across the chain.

``doActionFor`` resolves a transition id by walking the chain and taking the
**first** workflow that offers it. A id present in both workflows therefore
routes to the publication one and the provider workflow never moves -- with no
error to say so. The ids are asserted to be disjoint for that reason.
"""

from . import PROVIDER_CHAIN
from . import PROVIDER_WORKFLOW
from . import PUBLICATION_WORKFLOW
from collective.multiworkflow import api as mw_api
from plone import api
from plone.dexterity.content import DexterityContent

import pytest


class TestChain:
    def test_a_provider_runs_both_workflows(self, provider: DexterityContent):
        wt = api.portal.get_tool("portal_workflow")
        assert wt.getChainFor(provider) == PROVIDER_CHAIN

    def test_the_additional_workflow_is_appended_last(self, provider):
        """Order is not cosmetic: it decides first-match resolution."""
        wt = api.portal.get_tool("portal_workflow")
        assert wt.getChainFor(provider)[-1] == PROVIDER_WORKFLOW

    def test_states_are_reported_per_workflow(self, provider):
        assert mw_api.get_states(provider) == {
            PUBLICATION_WORKFLOW: "private",
            PROVIDER_WORKFLOW: "created",
        }


class TestTransitionIdsDoNotCollide:
    """A shared id would silently route to the publication workflow."""

    def test_no_id_is_offered_by_both(self, provider):
        wt = api.portal.get_tool("portal_workflow")
        publication = set(wt.getWorkflowById(PUBLICATION_WORKFLOW).transitions)
        provider_wf = set(wt.getWorkflowById(PROVIDER_WORKFLOW).transitions)
        assert publication & provider_wf == set()

    def test_every_provider_transition_is_owned_by_it(self, provider):
        owners = mw_api.owning_workflow(provider)
        wt = api.portal.get_tool("portal_workflow")
        for transition_id in wt.getWorkflowById(PROVIDER_WORKFLOW).transitions:
            assert owners[transition_id] == PROVIDER_WORKFLOW


class TestAvailableTransitions:
    def test_they_are_grouped_by_workflow(self, provider):
        available = mw_api.transitions(provider)
        assert set(available) == set(PROVIDER_CHAIN)

    def test_a_plain_organization_reports_one_workflow(self, plone_user):
        assert set(mw_api.transitions(plone_user)) == {PUBLICATION_WORKFLOW}

    def test_the_initial_state_offers_its_exits(self, provider):
        available = set(mw_api.transitions(provider)[PROVIDER_WORKFLOW])
        assert available == {"list", "verify", "archive", "review"}

    def test_they_follow_a_transition(self, provider, as_manager):
        as_manager(provider, "verify")
        available = set(mw_api.transitions(provider)[PROVIDER_WORKFLOW])
        assert available == {"archive", "review", "unverify"}


class TestTheWorkflowsMoveIndependently:
    """The whole point of the second workflow."""

    def test_a_provider_transition_leaves_the_page_private(self, provider, as_manager):
        as_manager(provider, "verify")
        assert api.content.get_state(obj=provider) == "private"

    def test_publishing_leaves_the_listing_in_created(self, provider):
        api.content.transition(obj=provider, transition="publish")
        assert mw_api.get_state(provider, workflow_id=PROVIDER_WORKFLOW) == "created"

    def test_a_published_page_can_hold_a_draft_listing(self, provider):
        """The combination that broke the old assumption that they are one."""
        api.content.transition(obj=provider, transition="publish")
        assert mw_api.get_states(provider) == {
            PUBLICATION_WORKFLOW: "published",
            PROVIDER_WORKFLOW: "created",
        }

    def test_and_a_private_page_can_hold_a_verified_listing(self, provider, as_manager):
        as_manager(provider, "verify")
        assert mw_api.get_states(provider) == {
            PUBLICATION_WORKFLOW: "private",
            PROVIDER_WORKFLOW: "verified",
        }


class TestGuards:
    """A guard that never denies is decoration."""

    def test_a_member_cannot_verify(self, provider):
        """`Manage Provider Listing` is not a role an organization holds."""
        with (
            api.env.adopt_roles(["Member"]),
            pytest.raises(api.exc.InvalidParameterError),
        ):
            api.content.transition(obj=provider, transition="verify")

    def test_a_member_cannot_list(self, provider):
        with (
            api.env.adopt_roles(["Member"]),
            pytest.raises(api.exc.InvalidParameterError),
        ):
            api.content.transition(obj=provider, transition="list")

    def test_a_member_sees_no_listing_transitions(self, provider):
        """A workflow with nothing available is omitted, not reported empty."""
        with api.env.adopt_roles(["Member"]):
            assert PROVIDER_WORKFLOW not in mw_api.transitions(provider)

    def test_a_reviewer_can_verify(self, provider):
        """Somebody has to be able to, or the workflow is a dead end."""
        with api.env.adopt_roles(["Reviewer"]):
            api.content.transition(obj=provider, transition="verify")
        assert mw_api.get_state(provider, workflow_id=PROVIDER_WORKFLOW) == "verified"
