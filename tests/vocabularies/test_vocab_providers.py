from collective.casestudy import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabProviders:

    name = f"{PACKAGE_NAME}.vocabulary.providers"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    @pytest.fixture(autouse=True)
    def _providers(self, providers):
        self.providers = providers

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    def test_token(self):
        tokens = {x for x in self.vocab.by_token}
        providers = {k for k in self.providers}
        assert tokens == providers

    def test_token_title(self):
        for token, expected in self.providers.items():
            term = self.vocab.getTerm(token)
        assert term.title == expected
