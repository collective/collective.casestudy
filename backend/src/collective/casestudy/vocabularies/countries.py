"""Country vocabularies.

Two of them, because a form and a filter want different things: a form has to
offer every country there is, while a facet listing must only offer the ones
some organization is actually in -- otherwise most choices return nothing.
"""

from collective.casestudy import _
from collective.casestudy import logger
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import pycountry


@provider(IVocabularyFactory)
def available_countries_vocabulary(context) -> SimpleVocabulary:
    """Vocabulary of all countries that could be used.

    :param context: Context the vocabulary is looked up on. Unused: the list
        of countries is the same everywhere.
    :returns: One term per ISO 3166-1 country, tokenised by alpha-2 code.
    """
    terms = []
    for country in pycountry.countries:
        terms.append(SimpleTerm(country.alpha_2, country.alpha_2, _(country.name)))
    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def countries_vocabulary(context) -> SimpleVocabulary:
    """Vocabulary of countries already used in the portal.

    Built from the ``country`` index, so it only ever offers a country some
    catalogued content is in.

    A code the index holds but pycountry does not know -- content indexed
    under an alpha-2 code ISO has since retired, or one written straight onto
    the object -- is logged and skipped. The alternative is an exception from
    a vocabulary every listing and every edit form looks up.

    :param context: Context the vocabulary is looked up on. Unused: the index
        is site-wide.
    :returns: One term per known country in use, tokenised by alpha-2 code.
    """
    terms = []
    ct = api.portal.get_tool("portal_catalog")
    for alpha_2 in ct.uniqueValuesFor("country"):
        country = pycountry.countries.get(alpha_2=alpha_2)
        if country is None:
            logger.warning(f"Ignoring unknown country code in the index: {alpha_2}")
            continue
        terms.append(SimpleTerm(country.alpha_2, country.alpha_2, _(country.name)))
    return SimpleVocabulary(terms)
