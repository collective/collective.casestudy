from collective.casestudy.behaviors.providers import IProviders
from plone import api
from plone.indexer import indexer


@indexer(IProviders)
def providers_indexer(obj):
    relations = obj.providers or []
    data = []
    for rel in relations:
        data.append(api.content.get_uuid(rel.to_object))
    return data
