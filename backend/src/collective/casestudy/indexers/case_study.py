"""Catalog indexers for the CaseStudy content type.

``industry`` and ``versions`` are plain schema fields; they need indexers only
because ``plone.indexer`` is how a Dexterity field reaches the catalog under
an index name of its own.
"""

from collective.casestudy.content.case_study import CaseStudy
from collective.casestudy.content.case_study import ICaseStudy
from plone.indexer import indexer


@indexer(ICaseStudy)
def industry_indexer(obj: CaseStudy) -> str:
    """Index the industry a case study belongs to.

    :param obj: The case study.
    :returns: The industry token.
    """
    return obj.industry


@indexer(ICaseStudy)
def versions_indexer(obj: CaseStudy) -> list[str]:
    """Index the Plone versions a case study covers.

    :param obj: The case study.
    :returns: The version tokens.
    """
    return obj.versions
