"""Reading relations, in the one place that knows how.

Four callers walk relations in this package -- an indexer, a serializer, a
subscriber and the facets indexer -- and every one of them needs the same
guard: a relation whose object has been deleted resolves to ``None``. Getting
that wrong is not a wrong answer but an ``AttributeError``, raised from
wherever the walk happens: a failed reindex, a failed save, a 500 on a page.
It has been the same bug three times, so the walk lives here now.

Relations are read from both ends. A case study *holds* a relation field and
resolves it forwards to its targets; an organization is *pointed at* and finds
its case studies backwards through the relation catalog.
"""

from collections.abc import Iterable
from collective.casestudy.content.case_study import CaseStudy
from collective.casestudy.content.organization import Organization
from plone import api
from plone.dexterity.content import DexterityContent
from z3c.relationfield.relation import RelationValue


#: Relation name to the key it is reported under. Read from the
#: organization's side: a ``providers`` relation is work it provided, an
#: ``organizations`` relation is coverage it received.
RELATIONSHIPS: dict[str, str] = {
    "providers": "provided",
    "organizations": "received",
}


def targets_of(relations: Iterable[RelationValue]) -> list[DexterityContent]:
    """Resolve relations forwards, to the objects they point at.

    :param relations: Relation values, typically a relation field's value.
    :returns: One object per relation that still resolves.
    """
    return [
        relation.to_object for relation in relations if relation.to_object is not None
    ]


def sources_of(relations: Iterable[RelationValue]) -> list[DexterityContent]:
    """Resolve relations backwards, to the objects that point at them.

    :param relations: Relation values, typically from the relation catalog.
    :returns: One object per relation that still resolves.
    """
    return [
        relation.from_object
        for relation in relations
        if relation.from_object is not None
    ]


def related_from_field(obj: DexterityContent, name: str) -> list[DexterityContent]:
    """Resolve a relation field on a content item.

    The field comes from a behavior, which a site may have switched off, and
    an unset relation list reads as ``None`` rather than as an empty one --
    hence the ``getattr`` and the ``or``.

    :param obj: Content carrying the relation field.
    :param name: Name of the relation field, e.g. ``organizations``.
    :returns: One object per relation that still resolves.
    """
    return targets_of(getattr(obj, name, None) or [])


def case_studies_for_organization(
    content: Organization,
) -> dict[str, list[CaseStudy]]:
    """Collect the case studies an organization takes part in.

    Looked up in the relation catalog rather than on the organization: the
    relations point *at* it, so there is nothing on the object itself to read.
    ``plone.api`` filters by the ``View`` permission of the current user, so
    an anonymous caller never learns about an unpublished case study.

    :param content: The organization.
    :returns: Mapping of every key in :data:`RELATIONSHIPS` to the case
        studies reaching it that way. Both keys are always present.
    """
    case_studies: dict[str, list[CaseStudy]] = {
        key: [] for key in RELATIONSHIPS.values()
    }
    for relationship, key in RELATIONSHIPS.items():
        relations = api.relation.get(target=content, relationship=relationship)
        case_studies[key] = sources_of(relations)
    return case_studies
