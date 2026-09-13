"""Keeping an organization's provider workflow in step with ``is_provider``.

``provider_workflow`` reaches an organization through
:class:`~collective.casestudy.behaviors.provider_info.IProvider`, a marker
`collective.multiworkflow` turns into an extra entry in the object's workflow
chain. Nothing sets that marker declaratively: ``is_provider`` is an ordinary
field, so an editor ticking the checkbox is what has to put the marker on --
and unticking it is what has to take the marker off again.

The role mappings are refreshed on every pass, not only when the marker
changes. A chain entry that arrives after the object was created has no role
mappings yet, and DCWorkflow answers a missing status with the workflow's
initial state rather than an error, so an object can sit in one state carrying
another state's security until something asks for the mappings to be rewritten.
"""

from collective.casestudy import logger
from collective.casestudy.behaviors.provider_info import IProvider
from collective.casestudy.content.organization import Organization
from collective.multiworkflow import api as mw_api
from plone import api
from Products.CMFPlone.WorkflowTool import WorkflowTool
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


WORKFLOW_ID: str = "provider_workflow"


def update_role_mappings(obj: Organization) -> None:
    """Rewrite the provider workflow's role mappings for an organization.

    Initialises the workflow for the object first, so it has a real status
    and a creation entry in its history rather than relying on DCWorkflow's
    silent fallback to ``initial_state`` for an object it has never seen.

    Applies the permission map of the state the object is *currently* in, so
    it is only correct once that state is known.

    :param obj: The organization whose security is rewritten.
    """
    wt: WorkflowTool = api.portal.get_tool("portal_workflow")
    workflow: DCWorkflowDefinition = wt.getWorkflowById(WORKFLOW_ID)
    # A workflow that joined the chain after the object was created was never
    # told the object exists, so it has no status and no history entry, and
    # ``updateRoleMappingsFor`` silently falls back to the initial state.
    # ``notifyCreated`` skips any workflow that already has history, so this
    # initialises the new one without disturbing the publication workflow.
    wt.notifyCreated(obj)
    workflow.updateRoleMappingsFor(obj)
    states = mw_api.get_states(obj)
    current_state = states.get(WORKFLOW_ID) or "-"
    logger.info(f"Updated role mappings for {obj.absolute_url()} - {current_state}")


def check_provider_status(obj: Organization) -> None:
    """Check the provider status for the organization.

    :param obj: The organization.
    """
    is_provider = obj.is_provider
    has_interface = IProvider.providedBy(obj)
    to_add = is_provider and not has_interface
    to_remove = not is_provider and has_interface
    if is_provider and not to_add:
        update_role_mappings(obj)
    elif not (to_add or to_remove):
        return
    elif to_add:
        alsoProvides(obj, IProvider)
        logger.info(f"Adding IProvider interface to {obj.absolute_url()}")
    elif to_remove:
        noLongerProvides(obj, IProvider)
        logger.info(f"Removing IProvider interface from {obj.absolute_url()}")
    update_role_mappings(obj)


def added(obj: Organization, event: IObjectAddedEvent) -> None:
    """Post creation handler for Organization.

    :param obj: The organization.
    :param event: The add event. Unused.
    """
    logger.info(f"Post creation handler triggered for {obj.absolute_url()}")
    check_provider_status(obj)


def modified(obj: Organization, event: IObjectModifiedEvent) -> None:
    """Post modification handler for Organization.

    :param obj: The organization.
    :param event: The modify event. Unused.
    """
    logger.info(f"Post modification handler triggered for {obj.absolute_url()}")
    check_provider_status(obj)
