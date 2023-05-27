from collective.casestudy import PACKAGE_NAME
from plone import api
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabAvailableCountries:

    name = f"{PACKAGE_NAME}.vocabulary.available_countries"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "BR",
            "GB",
            "RO",
            "US",
            "ES",
            "JP",
            "IT",
            "BE",
        ],
    )
    def test_token(self, token):
        assert token in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token,title",
        [
            ["BR", "Brazil"],
            ["GB", "United Kingdom"],
            ["RO", "Romania"],
            ["US", "United States"],
            ["ES", "Spain"],
            ["JP", "Japan"],
            ["IT", "Italy"],
            ["BE", "Belgium"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title


class TestVocabCountries:

    name = f"{PACKAGE_NAME}.vocabulary.countries"

    @pytest.fixture(autouse=True)
    def _init(self, get_vocabulary, portal, providers):
        for provider_uid in providers:
            obj = api.content.find(UID=provider_uid)[0].getObject()
            obj.reindexObject()
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "CH",
            "DE",
        ],
    )
    def test_token(self, token):
        assert token in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token",
        [
            "BR",
            "ES",
        ],
    )
    def test_token_not_in(self, token):
        assert token not in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token,title",
        [
            ["CH", "Switzerland"],
            ["DE", "Germany"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title
