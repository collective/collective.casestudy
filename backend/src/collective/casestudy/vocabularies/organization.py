"""How large an organization is, and what part it plays.

The size buckets come from the `casestudy.organization_sizes` registry record
rather than from code, like every other vocabulary this package offers a
control panel for. The tokens are still the half that must not change -- they
are stored on content -- but a site can now retitle a bucket, or add one,
without a release.

The facets are the exception: they are computed by an indexer and queried by
name, so a site adding one would get a term nothing ever indexes.
"""

from collective.casestudy import _
from collective.casestudy.vocabularies.terms import vocabulary_from_record
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


#: Registry record holding the size buckets.
SIZES_RECORD = "organization_sizes"


@provider(IVocabularyFactory)
def size_vocabulary(context) -> SimpleVocabulary:
    """Vocabulary of Organization sizes.

    :param context: Context the vocabulary is looked up on. Unused: the
        registry record is site-wide.
    :returns: One term per configured bucket, in record order.
    """
    return vocabulary_from_record(SIZES_RECORD)


#: Facet every organization carries.
DEFAULT_FACET = "Organization"

#: Facet added for an organization that opted in as a solution provider.
PROVIDER_FACET = "Provider"

#: Facet added for an organization that opted in as a site user.
USER_FACET = "User"


FACETS: dict[str, str] = {
    DEFAULT_FACET: _("Organization"),
    PROVIDER_FACET: _("Provider"),
    USER_FACET: _("User"),
}


@provider(IVocabularyFactory)
def facet_vocabulary(context) -> SimpleVocabulary:
    """Vocabulary of Organization facets.

    :param context: Context the vocabulary is looked up on. Unused: the
        buckets are fixed.
    :returns: One term per entry in :data:`FACETS`, in declaration order.
    """
    terms = []
    for token, title in FACETS.items():
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
