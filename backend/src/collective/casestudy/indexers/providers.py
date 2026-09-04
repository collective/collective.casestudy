"""Catalog indexer for the providers named by a content item.

The relation itself lives in the relation catalog, which answers "who points
at this provider" but not "which content names a provider" in a form
``portal_catalog`` can query -- so the UIDs are mirrored into an index of
their own. UIDs rather than paths, so the index survives a provider being
renamed or moved.
"""

from collective.casestudy.behaviors.providers import IProviders
from collective.casestudy.utils.relations import related_from_field
from plone import api
from plone.dexterity.content import DexterityContent
from plone.indexer import indexer


#: Relation field naming the providers of a content item.
PROVIDERS_FIELD = "providers"


@indexer(IProviders)
def providers_indexer(obj: DexterityContent) -> list[str]:
    """Index the UID of every provider related to this content.

    A relation whose target has been deleted is skipped by
    :func:`related_from_field` rather than indexed: it has no UID to record,
    and raising here would fail the reindex of the referencing content -- and,
    during a site-wide rebuild, of everything after it.

    :param obj: Content carrying the ``providers`` relation.
    :returns: One UID per relation that still resolves.
    """
    return [
        api.content.get_uuid(provider)
        for provider in related_from_field(obj, PROVIDERS_FIELD)
    ]
