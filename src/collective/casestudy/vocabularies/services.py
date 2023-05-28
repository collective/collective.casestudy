from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def services_vocabulary(context):
    """Vocabulary of Provider Services."""
    terms = []
    services = api.portal.get_registry_record("casestudy.services")
    for title in services:
        if "|" in title:
            token, title = title.split("|")
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
