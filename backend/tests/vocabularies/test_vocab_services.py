from collective.casestudy import PACKAGE_NAME
from plone.app.vocabularies import SimpleTerm
from plone.app.vocabularies import SimpleVocabulary

import pytest


class TestVocabServices:
    name: str = f"{PACKAGE_NAME}.vocabulary.services"
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
            ("design", "Design / Theming"),
            ("dev", "Development / Integration"),
            ("hosting", "Hosting"),
            ("training", "Training"),
        ],
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert isinstance(term, SimpleTerm)
        assert term.title == title
        assert term.token == token
