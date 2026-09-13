from collective.casestudy.content.case_study import CaseStudy
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


@pytest.fixture(scope="class")
def portal_type() -> str:
    return "CaseStudy"


@pytest.fixture(scope="class")
def payload(portal_type, case_studies_payload) -> dict:
    return case_studies_payload[0]


class TestCaseStudyFTI:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, portal_type, get_fti) -> None:
        """Bind the site and the FTI of the type under test to the instance."""
        self.portal = portal
        self.fti: DexterityFTI = get_fti(portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Case Study"),
            ("factory", "CaseStudy"),
            ("klass", "collective.casestudy.content.case_study.CaseStudy"),
            ("schema", "collective.casestudy.content.case_study.ICaseStudy"),
            ("add_permission", "cmf.AddPortalContent"),
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
            "collective.casestudy.providers",
            "collective.casestudy.organizations",
            "plone.dublincore",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
            "volto.blocks",
            "volto.navtitle",
            "volto.preview_image_link",
            "volto.head_title",
        )),
    )
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior

    def test_factory(self):
        """The FTI factory returns a CaseStudy."""
        obj = createObject(self.fti.factory)
        assert obj is not None
        assert isinstance(obj, CaseStudy)


class TestCaseStudy:
    def test_workflow_chain(self, portal_type, content_instance):
        """Case studies run a workflow of their own, not the site default."""
        wf_tool = api.portal.get_tool("portal_workflow")
        assert wf_tool.getChainFor(portal_type) == ("casestudy_workflow",)

    def test_create(self, portal_type, content_instance):
        """Content is created with the expected type and class."""
        assert content_instance.portal_type == portal_type
        assert isinstance(content_instance, CaseStudy)

    def test_indexer_industry(self, content_instance):
        """The industry field is indexed on creation."""
        brains = api.content.find(industry="ngo")
        assert len(brains) == 1
        assert content_instance.UID() == brains[0].UID
