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
        if "|" in title:
            token, title = title.split("|")
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
