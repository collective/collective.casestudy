"""Keeping an organization's facets in step with the case studies about it.

``USER_FACET`` is not stored on an organization -- it is derived from whether
any case study points at it through the ``organizations`` relation, and the
catalog only recomputes an object's indexes when *that object* is reindexed.
So a change to a case study has to reach across and reindex the organizations
it names, or a site that has just published its first case study still lists
that organization as one nobody has written about.

Only ``organizations`` is followed. The other facets do not depend on
relations: ``PROVIDER_FACET`` comes from a field on the organization itself,
so editing it already reindexes it.
"""

from collective.casestudy import logger
from collective.casestudy.content.case_study import CaseStudy
from collective.casestudy.content.organization import Organization
from collective.casestudy.utils.relations import related_from_field
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


#: Index recomputed on the organizations a case study names.
FACETS_INDEX = "facets"

#: Relation field naming the organizations a case study is about.
ORGANIZATIONS_FIELD = "organizations"


def related_organizations(obj: CaseStudy) -> list[Organization]:
    """Return the organizations a case study currently names.

    A relation whose target has been deleted is skipped by
    :func:`related_from_field`: it has nothing to reindex, and following it
    would raise from an event handler, which turns a stale relation into a
    case study that can no longer be saved.

    :param obj: The case study.
    :returns: One organization per relation that still resolves.
    """
    return related_from_field(obj, ORGANIZATIONS_FIELD)


def reindex_organization_facets(obj: CaseStudy) -> None:
    """Reindex the facets of organizations related to a case study.

    :param obj: The case study.
    """
    for organization in related_organizations(obj):
        logger.info(
            "Reindexing facets for organization %s due to case study %s",
            organization.Title(),
            obj.Title(),
        )
        organization.reindexObject(idxs=[FACETS_INDEX])


def added(obj: CaseStudy, event: IObjectAddedEvent) -> None:
    """Post creation handler for CaseStudy.

    :param obj: The case study.
    :param event: The add event. Unused.
    """
    reindex_organization_facets(obj)


def modified(obj: CaseStudy, event: IObjectModifiedEvent) -> None:
    """Post modification handler for CaseStudy.

    :param obj: The case study.
    :param event: The modify event. Unused.
    """
    reindex_organization_facets(obj)
