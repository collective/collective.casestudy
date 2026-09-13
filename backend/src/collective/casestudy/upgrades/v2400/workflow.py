"""Moving case studies onto ``casestudy_workflow``.

Case studies used to run ``simple_publication_workflow``. From 2400 they run a
workflow of their own, with the states of ``provider_workflow``, so an existing
case study needs a state in the new workflow that matches the one it had.

``plone.app.workflow.remap.remap_workflow`` -- what the Types control panel
uses -- is not a fit for an upgrade step. It reads the *old* state through the
chain the type has when it runs, and the ``workflow`` import step that precedes
this handler has already bound the type to the new workflow: every case study
would read as having no state and land in ``created``, published ones
included. So the old status is read here by workflow id instead.

The step is idempotent. A case study that already has a status in the new
workflow -- created after the import step ran, or migrated by an earlier run
-- is left alone.
"""

from collective.casestudy import logger
from DateTime import DateTime
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.WorkflowTool import WorkflowTool
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.GenericSetup.tool import SetupTool

import transaction


#: The type whose workflow changes.
PORTAL_TYPE = "CaseStudy"

#: The workflow case studies ran before 2400.
OLD_WORKFLOW_ID = "simple_publication_workflow"

#: The workflow case studies run from 2400.
WORKFLOW_ID = "casestudy_workflow"

#: Old state to new state. A state missing here lands in the new workflow's
#: initial state.
STATE_MAP: dict[str, str] = {
    "private": "created",
    "pending": "pending",
    "published": "listed",
}

#: Indexes that depend on the workflow state. ``workflow_states`` belongs to
#: `collective.multiworkflow`, and nothing else refreshes it for this change.
INDEXES: list[str] = ["allowedRolesAndUsers", "review_state", "workflow_states"]

#: Objects migrated between savepoints.
SAVEPOINT_EVERY = 100


def new_state_for(old_state: str | None, workflow: DCWorkflowDefinition) -> str:
    """Map a ``simple_publication_workflow`` state onto the new workflow.

    :param old_state: The state the case study had, or ``None`` if it had none.
    :param workflow: The new workflow, supplying the fallback initial state.
    :returns: The state the case study should have in the new workflow.
    """
    if old_state is None:
        return workflow.initial_state
    return STATE_MAP.get(old_state, workflow.initial_state)


def migrate_case_study(
    obj: DexterityContent, wt: WorkflowTool, workflow: DCWorkflowDefinition
) -> bool:
    """Give one case study a status in the new workflow.

    :param obj: The case study.
    :param wt: The workflow tool.
    :param workflow: The new workflow.
    :returns: ``True`` if the case study was migrated, ``False`` if it already
        had a status in the new workflow.
    """
    if wt.getStatusOf(WORKFLOW_ID, obj) is not None:
        return False
    old_status = wt.getStatusOf(OLD_WORKFLOW_ID, obj) or {}
    old_state = old_status.get("review_state")
    state = new_state_for(old_state, workflow)
    wt.setStatusOf(
        WORKFLOW_ID,
        obj,
        {
            "action": None,
            "actor": api.user.get_current().getId(),
            "comments": f"State migrated from {OLD_WORKFLOW_ID} ({old_state})",
            "review_state": state,
            "time": DateTime(),
        },
    )
    workflow.updateRoleMappingsFor(obj)
    obj.reindexObject(idxs=INDEXES)
    return True


def migrate_case_studies(context: SetupTool) -> None:
    """Move every case study onto ``casestudy_workflow``.

    :param context: The setup tool running the upgrade step. Unused.
    """
    wt: WorkflowTool = api.portal.get_tool("portal_workflow")
    workflow: DCWorkflowDefinition = wt.getWorkflowById(WORKFLOW_ID)
    brains = api.content.find(portal_type=PORTAL_TYPE, unrestricted=True)
    migrated = 0
    for brain in brains:
        obj = brain._unrestrictedGetObject()
        if not migrate_case_study(obj, wt, workflow):
            continue
        migrated += 1
        logger.info(f"-- {obj.absolute_url()}: {api.content.get_state(obj=obj)}")
        if migrated % SAVEPOINT_EVERY == 0:
            transaction.savepoint(optimistic=True)
    logger.info(f"Moved {migrated} of {len(brains)} case studies to {WORKFLOW_ID}")
