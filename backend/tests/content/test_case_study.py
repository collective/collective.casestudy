from collective.casestudy.content.case_study import CaseStudy
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "CaseStudy"


class TestCaseStudy:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, integration):
        self.fti = get_fti(CONTENT_TYPE)

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
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    def test_create(self, portal, case_studies_payload):
        payload = case_studies_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, CaseStudy)

    def test_indexer_industry(self, portal, case_studies_payload):
        payload = case_studies_payload[0]
        brains = api.content.find(industry="ngo")
        assert len(brains) == 0

        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)

        brains = api.content.find(industry="ngo")
        assert len(brains) == 1
        assert brains[0].Title == content.title
