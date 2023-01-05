from collective.casestudy import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabVersions:

    name = f"{PACKAGE_NAME}.vocabulary.versions"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "6.0",
            "5.2",
            "3.0",
        ],
    )
    def test_token(self, token):
        assert token in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token,title",
        [
            [
                "6.0",
                "Plone 6.0",
            ],
            [
                "5.2",
                "Plone 5.2",
            ],
            [
                "3.0",
                "Plone 3.0",
            ],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title
