"""Example content shipped with the package.

Imported through ``plone.exportimport`` from a folder exported by the
``update-example-content`` make target, so the fixture is regenerated from a
real site rather than maintained by hand.
"""

from collective.casestudy import logger
from pathlib import Path
from plone import api
from plone.exportimport import importers
from Products.CMFPlone.WorkflowTool import WorkflowTool
from Products.GenericSetup.tool import SetupTool


#: Folder holding the exported site the example content is imported from.
EXAMPLE_CONTENT_FOLDER = Path(__file__).parent / "examplecontent"


def create_example_content(portal_setup: SetupTool) -> None:
    """Import content available at the examplecontent folder.

    Role mappings are rewritten across the site once the import finishes.
    `plone.exportimport` restores an object's workflow state by assigning
    ``workflow_history`` directly, which fires no transition and so never
    updates the object's permission map. An additional workflow reaching the
    object through a marker interface is affected: it ends up in its restored
    state carrying the initial state's security. The sweep is site-wide
    because the importer gives no per-object hook that runs late enough.

    :param portal_setup: The setup tool running the import step. Unused: the
        site is resolved through :func:`plone.api.portal.get`.
    """
    portal = api.portal.get()
    importer = importers.get_importer(portal)
    for line in importer.import_site(EXAMPLE_CONTENT_FOLDER):
        logger.info(line)
    wt: WorkflowTool = api.portal.get_tool(name="portal_workflow")
    wt.updateRoleMappings()
    logger.info("Role mappings updated.")
