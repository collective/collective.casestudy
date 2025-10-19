from collective.casestudy.behaviors.provider_extras import IProviderExtras
from copy import deepcopy
from plone import api

import pytest


BEHAVIOR = "collective.casestudy.provider_extras"


@pytest.fixture
def portal(integration, get_fti):
    """Apply the provider_extras behavior on the Provider content type"""
    fti = get_fti("Provider")
    original_behaviors = fti.behaviors
    behaviors = [*list(original_behaviors), BEHAVIOR]
    fti.behaviors = tuple(behaviors)
    yield integration["portal"]
    # Revert changes
    fti.behaviors = original_behaviors


class TestProviderExtrasBehavior:
    def _create_provider(self, portal, providers_payload):
        payload = deepcopy(providers_payload[0])
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)

        return content

    def test_provider_extras_interface(self, portal, providers_payload):
        content = self._create_provider(portal, providers_payload)
        assert IProviderExtras.providedBy(content)
