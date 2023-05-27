from collective.casestudy import _
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


SIZES = [
    ("me", _("Just me")),
    ("small", _("Up to 5 employees")),
    ("medium", _("5 to 30 employees")),
    ("large", _("More than 30 employees")),
]


@provider(IVocabularyFactory)
def size_vocabulary(context):
    """Vocabulary of Organization sizes."""
    terms = []
    for token, title in SIZES:
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
