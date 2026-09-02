"""The organizations that can be named as solution providers.

Queried by facet rather than by ``portal_type``: every organization is one
type, and "is a provider" is a flag on the content that the ``facets`` index
carries.
"""

from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def providers_vocabulary(context) -> SimpleVocabulary:
    """Vocabulary of providers.

    :param context: Context the vocabulary is looked up on. Unused: the
        catalog query is site-wide.
    :returns: One term per organization flagged as a provider, tokenised by
        UID so a rename does not break stored values.
    """
    terms = []
    brains = api.content.find(portal_type="Organization", facets="Provider")
    for brain in brains:
        terms.append(SimpleTerm(brain.UID, brain.UID, brain.Title))
    return SimpleVocabulary(terms)
