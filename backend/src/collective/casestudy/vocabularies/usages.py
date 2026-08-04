from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def usages_vocabulary(context):
    """Vocabulary of Plone usages."""
    terms = []
    usages = api.portal.get_registry_record("casestudy.usages")
    for title in usages:
        token = title
        if "|" in title:
            token, title = title.split("|")
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
