from collective.casestudy.content.provider import Provider
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "Provider"


class TestProvider:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, integration):
        self.fti = get_fti(CONTENT_TYPE)

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Provider)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.categorization",
            "collective.casestudy.address_info",
            "collective.casestudy.contact_info",
            "volto.blocks",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    def test_create(self, portal, providers_payload):
        payload = providers_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Provider)
