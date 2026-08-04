from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def versions_vocabulary(context):
    """Vocabulary of Plone versions."""
    terms = []
    versions = api.portal.get_registry_record("casestudy.versions")
    for token in versions:
        title = f"Plone {token}"
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
