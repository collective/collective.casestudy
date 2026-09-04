from collective.casestudy import PACKAGE_NAME
from plone.app.vocabularies import SimpleTerm
from plone.app.vocabularies import SimpleVocabulary

import pytest


class TestVocabProviders:
    """Organizations flagged as providers are listed, keyed by UID."""

    name: str = f"{PACKAGE_NAME}.vocabulary.providers"
    vocab_type = SimpleVocabulary

    @pytest.fixture(autouse=True)
    def _setup(self, portal_class, get_vocabulary, providers_class):
        self.portal = portal_class
        self.providers = providers_class
        self.vocab = get_vocabulary(self.name, self.portal)

    def test_vocabulary_type(self):
        assert isinstance(self.vocab, self.vocab_type)

    def test_tokens(self):
        assert set(self.vocab.by_token) == set(self.providers)

    def test_vocab_terms(self):
        for token, title in self.providers.items():
            term = self.vocab.getTermByToken(token)
            assert isinstance(term, SimpleTerm)
            assert term.title == title
            assert term.token == token


class TestVocabProvidersExcludesPlainOrganizations:
    """Organizations that did not opt in as providers stay out of the listing."""

    name: str = f"{PACKAGE_NAME}.vocabulary.providers"
    vocab_type = SimpleVocabulary

    @pytest.fixture(autouse=True)
    def _setup(
        self, portal_class, get_vocabulary, organizations_class, providers_class
    ):
        self.portal = portal_class
        self.organizations = organizations_class
        self.providers = providers_class
        self.vocab = get_vocabulary(self.name, self.portal)

    def test_only_providers_are_listed(self):
        assert set(self.vocab.by_token) == set(self.providers)

    def test_plain_organizations_are_not_listed(self):
        tokens = set(self.vocab.by_token)
        for token in self.organizations:
            assert token not in tokens
