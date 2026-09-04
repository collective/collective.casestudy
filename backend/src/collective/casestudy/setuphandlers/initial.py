"""Example content shipped with the package.

Imported through ``plone.exportimport`` from a folder exported by the
``update-example-content`` make target, so the fixture is regenerated from a
real site rather than maintained by hand.
"""

from collective.casestudy import logger
from pathlib import Path
from plone import api
from plone.exportimport import importers
from Products.GenericSetup.tool import SetupTool


#: Folder holding the exported site the example content is imported from.
EXAMPLE_CONTENT_FOLDER = Path(__file__).parent / "examplecontent"


def create_example_content(portal_setup: SetupTool) -> None:
    """Import content available at the examplecontent folder.

    :param portal_setup: The setup tool running the import step. Unused: the
        site is resolved through :func:`plone.api.portal.get`.
    """
    portal = api.portal.get()
    importer = importers.get_importer(portal)
    for line in importer.import_site(EXAMPLE_CONTENT_FOLDER):
        logger.info(line)
