"""The ``provider_workflow`` definition, as installed.

A workflow is a graph, and GenericSetup imports it without checking that the
graph closes: a state may name an exit transition nobody defined, and a
transition may target a state that does not exist. Neither fails at install
time -- the first shows up as an action that is simply missing from the UI,
the second as a ``KeyError`` the moment somebody triggers it.

The permission maps get the same treatment. A ``permission-map`` naming a
permission the workflow does not manage is silently ignored, so a state that
looks locked down in the XML can be wide open in the site.
"""

from collective.casestudy.subscribers.organization import WORKFLOW_ID
from plone import api
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

import pytest


#: The permissions the workflow is expected to manage.
MANAGED_PERMISSIONS = {
    "collective.casestudy: Edit Provider Information",
    "collective.casestudy: View Provider Information",
    "collective.casestudy: Manage Provider Listing",
}

#: States whose permission map makes the provider fields publicly readable.
PUBLIC_STATES = {"listed", "verified", "archived"}


@pytest.fixture(scope="class")
def portal(portal_class):
    yield portal_class


@pytest.fixture
def workflow(portal) -> DCWorkflowDefinition:
    """The installed workflow definition."""
    wt = api.portal.get_tool("portal_workflow")
    return wt.getWorkflowById(WORKFLOW_ID)


class TestWorkflowInstalled:
    def test_workflow_exists(self, workflow):
        assert workflow is not None

    def test_it_is_not_bound_to_any_type(self, portal):
        """The chain adapter appends it; a type binding would double it up."""
        wt = api.portal.get_tool("portal_workflow")
        for portal_type in wt.listWorkflows():
            chain = wt.getChainForPortalType(portal_type)
            assert WORKFLOW_ID not in (chain or ())

    def test_state_variable(self, workflow):
        """A second workflow on one object needs its own state variable."""
        assert workflow.state_var == "workflow_states"

    def test_initial_state_exists(self, workflow):
        assert workflow.initial_state in workflow.states


class TestGraphCloses:
    """Every edge names something that exists."""

    def test_every_exit_transition_is_defined(self, workflow):
        defined = set(workflow.transitions)
        missing = {
            (state_id, transition_id)
            for state_id, state in workflow.states.items()
            for transition_id in state.transitions
            if transition_id not in defined
        }
        assert missing == set()

    def test_every_transition_targets_a_real_state(self, workflow):
        states = set(workflow.states)
        bad = {
            transition_id: transition.new_state_id
            for transition_id, transition in workflow.transitions.items()
            if transition.new_state_id and transition.new_state_id not in states
        }
        assert bad == {}

    def test_no_transition_is_unreachable(self, workflow):
        """A transition no state exits through can never be triggered."""
        reachable = {
            transition_id
            for state in workflow.states.values()
            for transition_id in state.transitions
        }
        assert set(workflow.transitions) - reachable == set()

    def test_every_state_is_reachable_from_the_initial_state(self, workflow):
        seen = {workflow.initial_state}
        queue = [workflow.initial_state]
        while queue:
            state = workflow.states[queue.pop()]
            for transition_id in state.transitions:
                target = workflow.transitions[transition_id].new_state_id
                if target and target not in seen:
                    seen.add(target)
                    queue.append(target)
        assert set(workflow.states) - seen == set()

    def test_no_state_is_a_dead_end(self, workflow):
        """Content that can never leave a state is content nobody can fix."""
        stuck = {
            state_id
            for state_id, state in workflow.states.items()
            if not state.transitions
        }
        assert stuck == set()


class TestPermissions:
    def test_managed_permissions(self, workflow):
        assert set(workflow.permissions) == MANAGED_PERMISSIONS

    def test_every_permission_map_is_managed(self, workflow):
        """A map for an unmanaged permission is silently ignored."""
        mapped = {
            permission
            for state in workflow.states.values()
            for permission in (state.permission_roles or {})
        }
        assert mapped - MANAGED_PERMISSIONS == set()

    def test_every_managed_permission_is_mapped_in_every_state(self, workflow):
        """An unmapped permission acquires, which is not what a map means."""
        for state_id, state in workflow.states.items():
            mapped = set(state.permission_roles or {})
            assert MANAGED_PERMISSIONS - mapped == set(), state_id

    @pytest.mark.parametrize("state_id", sorted(PUBLIC_STATES))
    def test_public_states_are_publicly_readable(self, workflow, state_id):
        roles = workflow.states[state_id].permission_roles[
            "collective.casestudy: View Provider Information"
        ]
        assert "Anonymous" in roles

    @pytest.mark.parametrize("state_id", ["created", "pending"])
    def test_draft_states_are_not_publicly_readable(self, workflow, state_id):
        roles = workflow.states[state_id].permission_roles[
            "collective.casestudy: View Provider Information"
        ]
        assert "Anonymous" not in roles

    def test_transitions_are_guarded(self, workflow):
        """An unguarded transition is one any authenticated user can fire."""
        unguarded = {
            transition_id
            for transition_id, transition in workflow.transitions.items()
            if not (transition.guard and transition.guard.permissions)
        }
        assert unguarded == set()
