from collective.casestudy.behaviors.providers import IProviders
from copy import deepcopy
from plone import api

import pytest


BEHAVIOR = "collective.casestudy.providers"


@pytest.fixture
def portal(integration, get_fti):
    """Apply the provider behavior on the CaseStudy content type"""
    fti = get_fti("CaseStudy")
    original_behaviors = fti.behaviors
    behaviors = [*list(original_behaviors), BEHAVIOR]
    fti.behaviors = tuple(behaviors)
    yield integration["portal"]
    # Revert changes
    fti.behaviors = original_behaviors


class TestProvidersBehavior:
    @pytest.fixture(autouse=True)
    def _providers(self, providers, portal):
        self.providers = providers

    @property
    def provider(self):
        provider_uid = next(iter(self.providers))
        return api.content.find(UID=provider_uid)[0].getObject()

    def _create_case_study_with_provider(self, portal, case_studies_payload):
        payload = deepcopy(case_studies_payload[0])
        provider = self.provider
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)

        # Create relation
        api.relation.create(content, provider, "providers")
        # Force reindex
        content.reindexObject(idxs=["providers"])
        return content

    def test_indexer_providers(self, portal, case_studies_payload):
        provider = self.provider
        provider_uid = api.content.get_uuid(provider)
        brains = api.content.find(providers=provider_uid)
        assert len(brains) == 0

        content = self._create_case_study_with_provider(portal, case_studies_payload)

        brains = api.content.find(providers=provider_uid)
        assert len(brains) == 1
        assert brains[0].Title == content.title

    def test_provides_interface(self, portal, case_studies_payload):
        content = self._create_case_study_with_provider(portal, case_studies_payload)
        assert IProviders.providedBy(content)

    def test_indexer_skips_a_deleted_provider(self, portal, case_studies_payload):
        """Deleting a provider must not break the reindex of its case studies.

        The relation stays on the case study with nothing behind it, so the
        indexer has no UID to record -- and raising here would fail every
        later object in a site-wide rebuild too.
        """
        content = self._create_case_study_with_provider(portal, case_studies_payload)
        provider = self.provider
        provider_uid = api.content.get_uuid(provider)
        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=provider, check_linkintegrity=False)

        # The reindex is what used to raise; `providers` is an index with no
        # metadata column, so the query is how its value is observed.
        content.reindexObject(idxs=["providers"])

        assert len(api.content.find(providers=provider_uid)) == 0

    def test_indexer_keeps_the_providers_that_remain(
        self, portal, case_studies_payload
    ):
        """Only the broken relation drops out, not the whole value."""
        content = self._create_case_study_with_provider(portal, case_studies_payload)
        provider = self.provider
        provider_uid = api.content.get_uuid(provider)
        second_uid = next(uid for uid in self.providers if uid != provider_uid)
        second = api.content.find(UID=second_uid)[0].getObject()
        api.relation.create(content, second, "providers")
        content.reindexObject(idxs=["providers"])

        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=provider, check_linkintegrity=False)
        content.reindexObject(idxs=["providers"])

        assert len(api.content.find(providers=provider_uid)) == 0
        found = api.content.find(providers=second_uid)
        assert len(found) == 1
        assert content.UID() == found[0].UID
