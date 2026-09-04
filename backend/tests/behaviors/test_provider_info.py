from collective.casestudy.vocabularies.organization import DEFAULT_FACET
from collective.casestudy.vocabularies.organization import PROVIDER_FACET
from plone import api

import pytest


BEHAVIOR = "collective.casestudy.provider_info"
CONTENT_TYPE = "Organization"


class TestProviderInfoBehavior:
    def test_behavior_enabled(self, integration, get_behaviors):
        assert BEHAVIOR in get_behaviors(CONTENT_TYPE)

    def test_is_provider_defaults_to_false(self, portal, organizations_payload):
        """An organization is a Plone user until it opts in as a provider."""
        payload = organizations_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)
        assert content.is_provider is False

    def test_facets_of_plain_organization(self, portal, organizations):
        """A plain organization carries the default facet, never the provider one."""
        for uid in organizations:
            brain = api.content.find(UID=uid)[0]
            assert brain.facets == [DEFAULT_FACET]

    def test_facets_of_provider(self, portal, providers):
        for uid in providers:
            brain = api.content.find(UID=uid)[0]
            assert DEFAULT_FACET in brain.facets
            assert PROVIDER_FACET in brain.facets

    @pytest.mark.parametrize(
        "facet,expected",
        [
            (DEFAULT_FACET, 2),
            (PROVIDER_FACET, 0),
        ],
    )
    def test_facets_index(self, portal, organizations, facet, expected):
        brains = api.content.find(portal_type=CONTENT_TYPE, facets=facet)
        assert len(brains) == expected

    def test_services_indexed(self, portal, providers):
        brains = api.content.find(services="hosting")
        assert len(brains) == 1
        assert brains[0].Title == "Company 2"
