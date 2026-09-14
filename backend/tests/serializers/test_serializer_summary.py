"""The site-wide summary metadata utility.

``facets`` is what a listing filters organizations by -- Plone user, provider,
or both -- so it has to survive into the summary a search returns. The utility
adds it to the default metadata fields for *every* summary, which is why the
assertions below are about catalog brains: that is the path listings take.
"""

from collective.casestudy.serializers.summary import JSONSummarySerializerMetadata
from collective.casestudy.vocabularies.organization import DEFAULT_FACET
from collective.casestudy.vocabularies.organization import PROVIDER_FACET
from collective.multiworkflow.utils.workflow import format_state
from plone import api
from plone.restapi.interfaces import IJSONSummarySerializerMetadata
from zope.component import getAllUtilitiesRegisteredFor

import pytest


class TestSummarySerializerMetadataUtility:
    """The utility itself, before any content exists."""

    def test_registered(self, portal):
        """The utility is registered by the package's ZCML."""
        utilities = getAllUtilitiesRegisteredFor(IJSONSummarySerializerMetadata)
        assert any(
            isinstance(utility, JSONSummarySerializerMetadata) for utility in utilities
        )

    def test_declares_facets(self):
        """It contributes exactly the one field."""
        assert JSONSummarySerializerMetadata().default_metadata_fields() == {"facets"}

    def test_facets_is_a_catalog_column(self, portal):
        """``getattr`` on a brain only works for a metadata column."""
        catalog = api.portal.get_tool("portal_catalog")
        assert "facets" in catalog.schema()


class TestSummaryOfBrains:
    """What a listing actually gets back."""

    @pytest.fixture
    def brain_for(self, portal):
        """Return a helper resolving a content item to its catalog brain."""

        def func(obj):
            return api.content.find(UID=obj.UID())[0]

        return func

    def test_organization_summary_has_facets(
        self, organization, brain_for, serialize_summary
    ):
        """A plain organization carries only the default facet."""
        data = serialize_summary(brain_for(organization))
        assert data["facets"] == [DEFAULT_FACET]

    def test_provider_summary_has_facets(self, provider, brain_for, serialize_summary):
        """A provider is both."""
        data = serialize_summary(brain_for(provider))
        assert sorted(data["facets"]) == sorted([DEFAULT_FACET, PROVIDER_FACET])

    def test_case_study_summary_has_facets_key(
        self, case_study, brain_for, serialize_summary
    ):
        """The field is site-wide, so it is present -- and empty -- elsewhere."""
        data = serialize_summary(brain_for(case_study))
        assert "facets" in data
        assert not data["facets"]

    def test_provider_summary_has_workflow_states(
        self, provider, brain_for, serialize_summary
    ):
        """`collective.multiworkflow` asks for the column in every summary."""
        data = serialize_summary(brain_for(provider))
        assert format_state("provider_workflow", "created") in data["workflow_states"]

    @pytest.mark.parametrize("key", ["@id", "@type", "title", "review_state"])
    def test_default_fields_untouched(
        self, organization, brain_for, serialize_summary, key: str
    ):
        """Adding a field must not drop the ones plone.restapi ships."""
        data = serialize_summary(brain_for(organization))
        assert key in data
