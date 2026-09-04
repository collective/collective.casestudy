from collective.casestudy import PACKAGE_NAME
from plone.app.vocabularies import SimpleTerm
from plone.app.vocabularies import SimpleVocabulary

import pytest


class TestVocabVersions:
    name: str = f"{PACKAGE_NAME}.vocabulary.versions"
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
            ("6.2", "Plone 6.2"),
            ("6.1", "Plone 6.1"),
            ("6.0", "Plone 6.0"),
            ("5.2", "Plone 5.2"),
            ("5.1", "Plone 5.1"),
            ("5.0", "Plone 5.0"),
            ("4.3", "Plone 4.3"),
            ("4.2", "Plone 4.2"),
            ("4.1", "Plone 4.1"),
            ("4.0", "Plone 4.0"),
            ("3.3", "Plone 3.3"),
            ("3.2", "Plone 3.2"),
            ("3.1", "Plone 3.1"),
            ("3.0", "Plone 3.0"),
            ("2.5", "Plone 2.5"),
            ("2.1", "Plone 2.1"),
            ("1.0", "Plone 1.0"),
        ],
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert isinstance(term, SimpleTerm)
        assert term.title == title
        assert term.token == token
