from collective.casestudy import PACKAGE_NAME
from plone.app.vocabularies import SimpleTerm
from plone.app.vocabularies import SimpleVocabulary

import pytest


class TestVocabOrganizationSize:
    name: str = f"{PACKAGE_NAME}.vocabulary.organization_size"
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
            ("me", "Just me"),
            ("small", "Up to 5 employees"),
            ("medium", "5 to 30 employees"),
            ("large", "More than 30 employees"),
        ],
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert isinstance(term, SimpleTerm)
        assert term.title == title
        assert term.token == token
