from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def industries_vocabulary(context):
    """Vocabulary of industries."""
    terms = []
    industries = api.portal.get_registry_record("casestudy.industries")
    for title in industries:
        terms.append(SimpleTerm(title, title, title))
    return SimpleVocabulary(terms)
