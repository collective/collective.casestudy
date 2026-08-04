from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def providers_vocabulary(context):
    """Vocabulary of providers."""
    terms = []
    brains = api.content.find(portal_type="Provider")
    for brain in brains:
        terms.append(SimpleTerm(brain.UID, brain.UID, brain.Title))
    return SimpleVocabulary(terms)
