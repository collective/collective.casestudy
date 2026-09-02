"""Removing the Provider content type.

Provider was superseded by Organization in profile version 2000 and kept
registered so existing content stayed openable. From 2200 it is gone: the
FTI, its workflow, and the permission to add one.

The removal is **conditional**. Deleting an FTI a site still has content for
leaves objects nothing can render or even delete cleanly, so this step counts
the Provider content first and, if it finds any, changes nothing and says so.
Migrating that content is a manual step -- there is no automatic conversion,
because deciding which organization a Provider becomes is an editorial call.
Once a site is clear, running this step again finishes the removal.
"""

from collective.casestudy import logger
from plone import api
from Products.GenericSetup.tool import SetupTool


#: The type this step removes.
PORTAL_TYPE = "Provider"

#: Workflow bound to it, used by nothing else.
WORKFLOW_ID = "provider_workflow"

#: Permission that guarded adding one.
ADD_PERMISSION = "collective.casestudy: Add Provider"


def provider_content(unrestricted: bool = True) -> list:
    """Return the brains of every Provider still in the site.

    :param unrestricted: Search past the current user's permissions, so
        private content is counted too.
    :returns: One brain per Provider.
    """
    return list(api.content.find(portal_type=PORTAL_TYPE, unrestricted=unrestricted))


def remove_provider_type(context: SetupTool) -> None:
    """Remove the Provider FTI, its workflow and its add permission.

    Nothing is removed while Provider content exists; see the module
    docstring for why, and for what to do about it.

    :param context: The setup tool running the upgrade step. Unused.
    """
    brains = provider_content()
    if brains:
        paths = ", ".join(brain.getPath() for brain in brains[:10])
        logger.warning(
            f"Not removing the {PORTAL_TYPE} type: {len(brains)} item(s) still "
            f"use it. Migrate them to Organization and run this upgrade step "
            f"again. First items: {paths}"
        )
        return

    # Unbind before the type goes, so the chain is not left pointing at a
    # portal type the tool can no longer resolve.
    workflow_tool = api.portal.get_tool("portal_workflow")
    if workflow_tool.getChainForPortalType(PORTAL_TYPE):
        workflow_tool.setChainForPortalTypes([PORTAL_TYPE], ())
        logger.info(f"-- unbound the {PORTAL_TYPE} workflow chain")
    if WORKFLOW_ID in workflow_tool:
        workflow_tool.manage_delObjects([WORKFLOW_ID])
        logger.info(f"-- removed the {WORKFLOW_ID} workflow")

    portal_types = api.portal.get_tool("portal_types")
    if PORTAL_TYPE in portal_types:
        portal_types.manage_delObjects([PORTAL_TYPE])
        logger.info(f"-- removed the {PORTAL_TYPE} type")

    try:
        api.portal.get().manage_permission(ADD_PERMISSION, roles=[], acquire=True)
        logger.info(f"-- reset the {ADD_PERMISSION!r} permission")
    except ValueError:
        # Zope only knows a permission while something registers it. With the
        # ZCML gone there may be nothing left to reset, which is the goal.
        logger.info(f"-- {ADD_PERMISSION!r} is no longer registered")

    logger.info("Upgrade concluded")
