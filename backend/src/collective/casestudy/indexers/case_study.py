from collective.casestudy.content.case_study import ICaseStudy
from plone.indexer import indexer


@indexer(ICaseStudy)
def industry_indexer(obj):
    return obj.industry


@indexer(ICaseStudy)
def versions_indexer(obj):
    return obj.versions
