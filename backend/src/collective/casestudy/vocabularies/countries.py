"""Country vocabularies.

Two of them, because a form and a filter want different things: a form has to
offer every country there is, while a facet listing must only offer the ones
some organization is actually in -- otherwise most choices return nothing.

Both are sorted by the country name in the current language, so a translated
list reads alphabetically instead of in pycountry's order.
"""

from collections.abc import Iterable
from collective.casestudy import _country
from collective.casestudy import logger
from plone import api
from zope.i18n import translate
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import pycountry
import unicodedata


def _sort_key(text: str) -> str:
    """Key ignoring case and accents, so "Áustria" sorts before "Bélgica".

    :param text: A translated country name.
    :returns: The name decomposed, stripped of combining marks and casefolded.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()


def _vocabulary(countries: Iterable) -> SimpleVocabulary:
    """Build a vocabulary of countries sorted by their translated name.

    The titles stay translatable messages, so whoever renders them still
    translates them; the translation here only decides the order.

    :param countries: pycountry country records.
    :returns: One term per country, tokenised by alpha-2 code.
    """
    language = api.portal.get_current_language()
    terms = [
        SimpleTerm(country.alpha_2, country.alpha_2, _country(country.name))
        for country in countries
    ]
    terms.sort(key=lambda t: _sort_key(translate(t.title, target_language=language)))
    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def available_countries_vocabulary(context) -> SimpleVocabulary:
    """Vocabulary of all countries that could be used.

    :param context: Context the vocabulary is looked up on. Unused: the list
        of countries is the same everywhere.
    :returns: One term per ISO 3166-1 country, tokenised by alpha-2 code.
    """
    return _vocabulary(pycountry.countries)


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
    countries = []
    ct = api.portal.get_tool("portal_catalog")
    for alpha_2 in ct.uniqueValuesFor("country"):
        country = pycountry.countries.get(alpha_2=alpha_2)
        if country is None:
            logger.warning(f"Ignoring unknown country code in the index: {alpha_2}")
            continue
        countries.append(country)
    return _vocabulary(countries)
