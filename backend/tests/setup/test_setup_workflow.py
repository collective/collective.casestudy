"""The workflow definitions this package ships, as installed.

A workflow is a graph, and GenericSetup imports it without checking that the
graph closes: a state may name an exit transition nobody defined, and a
transition may target a state that does not exist. Neither fails at install
time -- the first shows up as an action that is simply missing from the UI,
the second as a ``KeyError`` the moment somebody triggers it.

The permission maps get the same treatment. A ``permission-map`` naming a
permission the workflow does not manage is silently ignored, so a state that
looks locked down in the XML can be wide open in the site.

Both workflows go through the same checks. ``provider_workflow`` is appended
to an organization by the chain adapter; ``casestudy_workflow`` is bound to
``CaseStudy``. They share their states, and differ in the permissions they
manage and in the state variable they keep.
"""

from collective.casestudy.subscribers.organization import WORKFLOW_ID
from plone import api
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

import pytest


#: What each workflow is expected to look like once installed: the
#: permissions it manages, the one gating public reading, its state variable,
#: and the portal types it is bound to.
WORKFLOWS: dict[str, dict] = {
    WORKFLOW_ID: {
        "permissions": {
            "collective.casestudy: Edit Provider Information",
            "collective.casestudy: View Provider Information",
            "collective.casestudy: Manage Provider Listing",
        },
        "view": "collective.casestudy: View Provider Information",
        "state_var": "workflow_states",
        "types": set(),
    },
    "casestudy_workflow": {
        "permissions": {
            "Access contents information",
            "Modify portal content",
            "View",
        },
        "view": "View",
        "state_var": "review_state",
        "types": {"CaseStudy"},
    },
}

#: States whose permission map makes the content publicly readable.
PUBLIC_STATES = {"listed", "verified", "archived"}

#: States whose permission map keeps the content staff-only.
DRAFT_STATES = {"created", "pending"}


@pytest.fixture(scope="class")
def portal(portal_class):
    yield portal_class


@pytest.fixture(params=sorted(WORKFLOWS))
def workflow_id(request) -> str:
    """Id of the workflow under test; every test runs once per workflow."""
    return request.param


@pytest.fixture
def expected(workflow_id: str) -> dict:
    """What the workflow under test is expected to look like."""
    return WORKFLOWS[workflow_id]


@pytest.fixture
def workflow(portal, workflow_id: str) -> DCWorkflowDefinition:
    """The installed workflow definition."""
    wt = api.portal.get_tool("portal_workflow")
    return wt.getWorkflowById(workflow_id)


class TestWorkflowInstalled:
    def test_workflow_exists(self, workflow):
        assert workflow is not None

    def test_bound_types(self, portal, workflow_id, expected):
        """``provider_workflow`` is appended by the chain adapter, never bound.

        A type binding would double it up on every provider.
        """
        wt = api.portal.get_tool("portal_workflow")
        portal_types = api.portal.get_tool("portal_types")
        bound = {
            portal_type
            for portal_type in portal_types.listContentTypes()
            if workflow_id in (wt.getChainForPortalType(portal_type) or ())
        }
        assert bound == expected["types"]

    def test_state_variable(self, workflow, expected):
        """A second workflow on one object needs a state variable of its own.

        A type's own workflow keeps ``review_state``, which is what listings
        and the ``review_state`` index read.
        """
        assert workflow.state_var == expected["state_var"]

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
    def test_managed_permissions(self, workflow, expected):
        assert set(workflow.permissions) == expected["permissions"]

    def test_every_permission_map_is_managed(self, workflow, expected):
        """A map for an unmanaged permission is silently ignored."""
        mapped = {
            permission
            for state in workflow.states.values()
            for permission in (state.permission_roles or {})
        }
        assert mapped - expected["permissions"] == set()

    def test_every_managed_permission_is_mapped_in_every_state(
        self, workflow, expected
    ):
        """An unmapped permission acquires, which is not what a map means."""
        for state_id, state in workflow.states.items():
            mapped = set(state.permission_roles or {})
            assert expected["permissions"] - mapped == set(), state_id

    @pytest.mark.parametrize("state_id", sorted(PUBLIC_STATES))
    def test_public_states_are_publicly_readable(self, workflow, expected, state_id):
        roles = workflow.states[state_id].permission_roles[expected["view"]]
        assert "Anonymous" in roles

    @pytest.mark.parametrize("state_id", sorted(DRAFT_STATES))
    def test_draft_states_are_not_publicly_readable(self, workflow, expected, state_id):
        roles = workflow.states[state_id].permission_roles[expected["view"]]
        assert "Anonymous" not in roles

    def test_transitions_are_guarded(self, workflow):
        """An unguarded transition is one any authenticated user can fire."""
        unguarded = {
            transition_id
            for transition_id, transition in workflow.transitions.items()
            if not (transition.guard and transition.guard.permissions)
        }
        assert unguarded == set()


class TestCaseStudyWorkflowMirrorsProvider:
    """``casestudy_workflow`` is meant to move through the same states."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        wt = api.portal.get_tool("portal_workflow")
        self.provider: DCWorkflowDefinition = wt.getWorkflowById(WORKFLOW_ID)
        self.case_study: DCWorkflowDefinition = wt.getWorkflowById("casestudy_workflow")

    def test_same_states(self):
        assert set(self.case_study.states) == set(self.provider.states)

    def test_same_initial_state(self):
        assert self.case_study.initial_state == self.provider.initial_state

    def test_same_transitions(self):
        """Same ids, leading to the same states."""

        def edges(workflow: DCWorkflowDefinition) -> dict[str, str]:
            return {
                transition_id: transition.new_state_id
                for transition_id, transition in workflow.transitions.items()
            }

        assert edges(self.case_study) == edges(self.provider)

    def test_same_exits_per_state(self):
        for state_id, state in self.provider.states.items():
            case_study_state = self.case_study.states[state_id]
            assert set(case_study_state.transitions) == set(state.transitions), state_id
