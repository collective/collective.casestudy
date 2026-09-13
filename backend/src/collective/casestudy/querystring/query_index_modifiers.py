"""Query modifiers for the listing and verification querystring fields.

Each field is a Yes/No criterion, and its modifier rewrites it onto
`collective.multiworkflow`'s ``workflow_states`` index, whose values read
``<workflow-id>|<state-id>``:

* *Yes* matches the states the field stands for: ``verified`` for the verified
  fields, ``listed`` or ``verified`` for the listed ones.
* *No* matches every other state of the same workflow.

Both only ever name states of the field's own workflow, so content that does
not run it -- a plain organization, a document, a case study for a provider
field -- matches neither.

**Known limitation.** All four fields, and `collective.multiworkflow`'s own
``review_state`` modifier, target the same index. ``plone.app.querystring``
stores a rewritten criterion under its new index name, so when a query holds
two of them the last modifier to run replaces the other one, without an error.
A single ``KeywordIndex`` criterion cannot express "listed or verified, and
published".
"""

from collective.multiworkflow.indexers import format_state
from collective.multiworkflow.indexers import WORKFLOW_STATES
from plone import api
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from Products.CMFPlone.WorkflowTool import WorkflowTool
from typing import Any
from zope.interface import implementer


#: Workflow the case study fields filter on.
CASESTUDY_WORKFLOW = "casestudy_workflow"

#: Workflow the provider fields filter on.
PROVIDER_WORKFLOW = "provider_workflow"

#: States a *Yes* on a verified field matches.
VERIFIED_STATES: tuple[str, ...] = ("verified",)

#: States a *Yes* on a listed field matches. Verified content is listed too.
LISTED_STATES: tuple[str, ...] = ("listed", *VERIFIED_STATES)


@implementer(IParsedQueryIndexModifier)
class WorkflowStatesModifier:
    """Rewrite a Yes/No criterion onto the states of one workflow."""

    def __init__(self, workflow_id: str, states: tuple[str, ...]) -> None:
        """Bind the modifier to a workflow and the states *Yes* stands for.

        :param workflow_id: Id of the workflow whose states are matched.
        :param states: State ids a *Yes* matches.
        """
        self.workflow_id = workflow_id
        self.states = states

    def other_states(self) -> list[str]:
        """Return the states of the workflow that *Yes* does not match.

        Read from the installed workflow rather than listed here, so a state
        added to the definition later is covered by *No* without a code change.

        :returns: State ids; empty when the workflow is not installed, which
            makes *No* match nothing rather than everything.
        """
        wt: WorkflowTool = api.portal.get_tool("portal_workflow")
        workflow = wt.getWorkflowById(self.workflow_id)
        if workflow is None:
            return []
        return [state for state in workflow.states if state not in self.states]

    def __call__(self, value: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Replace the Yes/No criterion with the states it stands for.

        :param value: The parsed criterion, ``{"query": True}`` or
            ``{"query": False}``.
        :returns: ``workflow_states`` and a criterion naming the matched
            states, qualified with the workflow id.
        """
        states = self.states if value.get("query") else self.other_states()
        return (
            WORKFLOW_STATES,
            {"query": [format_state(self.workflow_id, state) for state in states]},
        )


#: Modifier for the ``case_study_verified`` field.
case_study_verified = WorkflowStatesModifier(CASESTUDY_WORKFLOW, VERIFIED_STATES)

#: Modifier for the ``case_study_listed`` field.
case_study_listed = WorkflowStatesModifier(CASESTUDY_WORKFLOW, LISTED_STATES)

#: Modifier for the ``provider_verified`` field.
provider_verified = WorkflowStatesModifier(PROVIDER_WORKFLOW, VERIFIED_STATES)

#: Modifier for the ``provider_listed`` field.
provider_listed = WorkflowStatesModifier(PROVIDER_WORKFLOW, LISTED_STATES)
