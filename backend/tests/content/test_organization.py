from collective.casestudy.content.organization import Organization
from collective.casestudy.vocabularies.organization import DEFAULT_FACET
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


@pytest.fixture(scope="class")
def portal_type() -> str:
    return "Organization"


@pytest.fixture(scope="class")
def payload(portal_type, organizations_payload) -> dict:
    return organizations_payload[0]


class TestOrganizationFTI:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, portal_type, get_fti) -> None:
        """Bind the site and the FTI of the type under test to the instance."""
        self.portal = portal
        self.fti: DexterityFTI = get_fti(portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Organization"),
            ("factory", "Organization"),
            ("klass", "collective.casestudy.content.organization.Organization"),
            ("schema", "collective.casestudy.content.organization.IOrganization"),
            ("add_permission", "collective.casestudy.organization.add"),
            ("global_allow", True),
        ],
    )
    def test_fti(self, attr: str, expected):
        """Test FTI values."""
        fti = self.fti

        assert isinstance(fti, DexterityFTI)
        assert getattr(fti, attr) == expected

    @pytest.mark.parametrize(
        "idx,behavior",
        enumerate((
            "plone.basic",
            "volto.preview_image_link",
            "collective.casestudy.contact_info",
            "plonegovbr.socialmedia.links",
            "collective.casestudy.address_info",
            "collective.casestudy.provider_info",
            "plone.categorization",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
        )),
    )
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior

    def test_factory(self):
        """The FTI factory returns an Organization."""
        obj = createObject(self.fti.factory)
        assert obj is not None
        assert isinstance(obj, Organization)

    def test_addable_at_portal_root(self, portal_type):
        """Organization replaces Provider as the globally addable type."""
        addable = [fti.getId() for fti in self.portal.allowedContentTypes()]
        assert portal_type in addable

    def test_workflow_chain(self, portal_type):
        """Organization uses the site default workflow.

        Contact information is protected by the acquired rolemap grants
        rather than by per-state permission maps, so no workflow of its own
        is needed.
        """
        wf_tool = api.portal.get_tool("portal_workflow")
        assert wf_tool.getChainFor(portal_type) == ("simple_publication_workflow",)


class TestOrganization:
    def test_create(self, portal_type, content_instance):
        """Content is created with the expected type and class."""
        assert content_instance.portal_type == portal_type
        assert isinstance(content_instance, Organization)

    def test_indexer_facets(self, content_instance):
        """A plain organization gets the default facet, not the provider one."""
        brain = api.content.find(UID=content_instance.UID())[0]
        assert brain.facets == [DEFAULT_FACET]
