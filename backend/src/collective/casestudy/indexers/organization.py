"""Catalog indexer for the roles an organization plays.

Every organization in the site is a Plone user; being a solution provider is
an opt-in extra. Indexing both under one keyword index means a listing filters
on either without the site needing a second index, and an organization that is
both appears in both listings.
"""

from collective.casestudy.content.organization import IOrganization
from collective.casestudy.content.organization import Organization
from collective.casestudy.utils.relations import case_studies_for_organization
from collective.casestudy.vocabularies.organization import DEFAULT_FACET
from collective.casestudy.vocabularies.organization import PROVIDER_FACET
from collective.casestudy.vocabularies.organization import USER_FACET
from plone.indexer import indexer


@indexer(IOrganization)
def facets_indexer(obj: Organization) -> list[str]:
    """Index the facets of an organization.

    ``is_provider`` comes from the ``provider_info`` behavior, which a site
    may have switched off -- hence the ``getattr`` rather than an attribute
    access that would break indexing.

    :param obj: The organization.
    :returns: The facet tokens, always including :data:`DEFAULT_FACET`.
    """
    facets = [DEFAULT_FACET]
    # Check if the organization is also a provider
    if getattr(obj, "is_provider", False):
        facets.append(PROVIDER_FACET)
    case_studies = case_studies_for_organization(obj)
    if case_studies["received"]:
        facets.append(USER_FACET)
    return facets
