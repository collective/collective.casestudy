"""Tests for the upgrade path of the ``collective.casestudy:default`` profile.

A profile file is only half a change: the matching GenericSetup import step has
to be re-run by an upgrade, or the change reaches fresh installs only.
"""

from collections.abc import Callable
from collective.casestudy import PACKAGE_NAME
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.GenericSetup.tool import SetupTool

import pytest


PROFILE_ID = f"{PACKAGE_NAME}:default"


@pytest.fixture(scope="class")
def portal(portal_class):
    yield portal_class


class TestUpgradeImportSteps:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, setup_tool: SetupTool) -> None:
        self.portal = portal
        self.setup_tool = setup_tool

    @pytest.fixture
    def upgrade_import_steps(self) -> Callable[[str, str], set[str]]:
        """Return a getter for the import steps re-run by an upgrade.

        :returns: Callable taking the source and destination profile versions
            and returning the set of import step ids re-run between them.
        """

        def func(source: str, destination: str) -> set[str]:
            steps = self.setup_tool.listUpgrades(PROFILE_ID, show_old=True, simple=True)
            return {
                step_id
                for step in steps
                if step.source == (source,) and step.dest == (destination,)
                for step_id in getattr(step, "import_steps", ())
            }

        return func

    def test_registered_import_steps_exist(self, upgrade_import_steps):
        """Every import step named by an upgrade must be a registered step.

        ``import_steps`` is a ``zope.configuration.fields.Tokens`` field, so it
        splits on whitespace and **not** on commas: ``import_steps="a,b"`` is
        the single unknown step ``"a,b"``, and running it raises ``ValueError``.
        """
        known = set(self.setup_tool.listImportSteps())
        declared = set()
        for step in self.setup_tool.listUpgrades(
            PROFILE_ID, show_old=True, simple=True
        ):
            declared.update(getattr(step, "import_steps", ()))
        assert declared - known == set()

    def test_querystring_fields_reach_existing_sites(self):
        """The listing and verification querystring fields need a registry import.

        They were added after profile version 2300, along with new groups for
        the existing fields. ``registry/*.xml`` is only read on install, so an
        upgrade starting at 2300 or later has to re-run ``plone.app.registry``.
        """
        steps = self.setup_tool.listUpgrades(PROFILE_ID, show_old=True, simple=True)
        rerun = {
            step.dest
            for step in steps
            if int(step.source[0]) >= 2300
            and "plone.app.registry" in getattr(step, "import_steps", ())
        }
        assert rerun != set()

    @pytest.mark.parametrize(
        "source,destination,import_step",
        [
            ("1000", "1100", "typeinfo"),
            ("1000", "1100", "rolemap"),
            ("1000", "1100", "workflow"),
            ("1000", "1100", "catalog"),
            ("1000", "1100", "difftool"),
            ("1000", "1100", "repositorytool"),
            ("1000", "1100", "plone.app.registry"),
            ("1100", "1200", "plone.app.registry"),
            # Organization: new type, permissions, workflow bindings ...
            ("1200", "2000", "typeinfo"),
            ("1200", "2000", "rolemap"),
            ("1200", "2000", "workflow"),
            # ... the facets index and column backing the providers vocabulary
            ("1200", "2000", "catalog"),
            # ... and its versioning policies
            ("1200", "2000", "repositorytool"),
        ],
    )
    def test_upgrade_reruns_import_step(
        self,
        upgrade_import_steps,
        source: str,
        destination: str,
        import_step: str,
    ):
        """Test an upgrade re-runs the import step a profile change needs."""
        assert import_step in upgrade_import_steps(source, destination)


class TestCatalog:
    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        self.portal = portal
        self.catalog: CatalogTool = portal.portal_catalog

    @pytest.mark.parametrize(
        "name,meta_type",
        [
            ("country", "FieldIndex"),
            ("facets", "KeywordIndex"),
            ("industry", "FieldIndex"),
            ("providers", "KeywordIndex"),
            ("services", "KeywordIndex"),
            ("usages", "KeywordIndex"),
            ("versions", "KeywordIndex"),
        ],
    )
    def test_index(self, name: str, meta_type: str):
        """Test an index declared in ``catalog.xml`` is installed."""
        assert name in self.catalog.indexes()
        assert self.catalog._catalog.getIndex(name).meta_type == meta_type

    @pytest.mark.parametrize(
        "name",
        [
            "country",
            "facets",
            "industry",
            "services",
            "usages",
            "versions",
        ],
    )
    def test_column(self, name: str):
        """Test a metadata column declared in ``catalog.xml`` is installed."""
        assert name in self.catalog.schema()
