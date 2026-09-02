"""The industries a case study can be filed under.

Editable per site: the terms come from the `casestudy.industries` registry
record rather than from code.
"""

from collective.casestudy.vocabularies.terms import vocabulary_from_record
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def industries_vocabulary(context) -> SimpleVocabulary:
    """Vocabulary of industries a case study can be filed under.

    :param context: Context the vocabulary is looked up on. Unused: the
        registry record is site-wide.
    :returns: One term per configured entry, in record order.
    """
    return vocabulary_from_record("industries")
