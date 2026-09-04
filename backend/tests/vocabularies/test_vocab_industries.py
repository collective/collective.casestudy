from collective.casestudy import PACKAGE_NAME
from plone.app.vocabularies import SimpleTerm
from plone.app.vocabularies import SimpleVocabulary

import pytest


class TestVocabIndustries:
    name: str = f"{PACKAGE_NAME}.vocabulary.industries"
    vocab_type = SimpleVocabulary

    @pytest.fixture(autouse=True)
    def _setup(self, portal_class, get_vocabulary):
        self.portal = portal_class
        self.vocab = get_vocabulary(self.name, self.portal)

    def test_vocabulary_type(self):
        assert isinstance(self.vocab, self.vocab_type)

    @pytest.mark.parametrize(
        "token,title",
        [
            ("edu", "University & Education"),
            ("ngo", "Non-Profit & NGO"),
            ("oil-gas", "Oil & Gas"),
            ("gov", "Government & Public Sector"),
            ("finance", "Finance & Banking"),
            ("healthcare", "Healthcare & Life Sciences"),
            ("media", "Media & Publishing"),
            ("transport", "Transport & Logistics"),
            ("retail", "Retail & E-commerce"),
            ("technology", "Technology & IT Services"),
            ("legal", "Legal Services"),
            ("professional-services", "Professional Services"),
            ("manufacturing", "Manufacturing & Industry"),
            ("energy", "Energy & Utilities"),
            ("telecom", "Telecommunications"),
            ("corporate", "Corporate"),
        ],
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert isinstance(term, SimpleTerm)
        assert term.title == title
        assert term.token == token

    def test_offered_in_record_order(self):
        """The record's order is the order the form offers the terms in."""
        assert [term.token for term in self.vocab][:3] == ["edu", "ngo", "oil-gas"]

    def test_corporate_survived_the_retitling(self):
        """It is not in the shipped list any more, but content still uses it.

        Dropping a token orphans every case study filed under it, so the term
        stays even though nothing new is expected to choose it.
        """
        assert self.vocab.getTermByToken("corporate").title == "Corporate"
