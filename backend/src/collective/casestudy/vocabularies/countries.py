from collective.casestudy import _
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import pycountry


@provider(IVocabularyFactory)
def available_countries_vocabulary(context):
    """Vocabulary of all countries that could be used."""
    terms = []
    for country in pycountry.countries:
        terms.append(SimpleTerm(country.alpha_2, country.alpha_2, _(country.name)))
    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def countries_vocabulary(context):
    """Vocabulary of countries already used in the portal."""
    terms = []
    ct = api.portal.get_tool("portal_catalog")
    for alpha_2 in ct.uniqueValuesFor("country"):
        country = pycountry.countries.get(alpha_2=alpha_2)
        terms.append(SimpleTerm(country.alpha_2, country.alpha_2, _(country.name)))
    return SimpleVocabulary(terms)
