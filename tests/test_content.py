from collective.casestudy.content.case_study import CaseStudy
from plone import api
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import pytest


CONTENT_TYPE = "CaseStudy"


@pytest.fixture
def payload() -> dict:
    """Payload to create a new Case Study."""
    return {
        "type": CONTENT_TYPE,
        "title": "New Plone.org",
        "description": "An explanation about the new Plone.org",
        "subject": ["Tag 1", "Tag 2"],
        "industry": "NGO",
        "remoteUrl": "https://plone.org",
        "id": "plone-org",
    }


class TestCaseStudy:
    @pytest.fixture(autouse=True)
    def _fti(self, integration):
        self.fti = queryUtility(IDexterityFTI, name=CONTENT_TYPE)

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, CaseStudy)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.dublincore",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
            "volto.blocks",
            "volto.navtitle",
            "volto.preview_image",
            "volto.head_title",
        ],
    )
    def test_has_behavior(self, behavior):
        assert behavior in list(self.fti.behaviors)

    def test_create(self, portal, payload):
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, CaseStudy)

    def test_indexer_industry(self, portal, payload):
        brains = api.content.find(industry="NGO")
        assert len(brains) == 0

        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)

        brains = api.content.find(industry="NGO")
        assert len(brains) == 1
        assert brains[0].Title == content.title
