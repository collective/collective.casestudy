"""Extra metadata every summary in the site carries.

``facets`` is how a listing tells organizations apart -- Plone user, solution
provider, or both -- and it is computed by
:func:`collective.casestudy.indexers.organization.facets_indexer`. It is a
catalog column, but plone.restapi only serializes the columns some
:class:`IJSONSummarySerializerMetadata` utility asks for, so without this the
field would be in the catalog and absent from every search result.

The contribution is site-wide rather than per type: summaries are built from
brains, which have no type-specific serializer to hook into. Content with no
``facets`` reports an empty value, which is what a filter expects anyway.
"""

from plone.restapi.interfaces import IJSONSummarySerializerMetadata
from zope.interface import implementer


@implementer(IJSONSummarySerializerMetadata)
class JSONSummarySerializerMetadata:
    """Additional metadata to be exposed on listings."""

    def default_metadata_fields(self) -> set[str]:
        """Name the catalog columns to add to every summary.

        :returns: The set of extra field names.
        """
        return {"facets", "workflow_states"}
