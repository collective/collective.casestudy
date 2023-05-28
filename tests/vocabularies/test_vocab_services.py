from collective.casestudy import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabServices:

    name = f"{PACKAGE_NAME}.vocabulary.services"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "design",
            "dev",
            "hosting",
            "training",
        ],
    )
    def test_token(self, token):
        assert token in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token, title",
        [
            ["design", "Design / Theming"],
            ["dev", "Development / Integration"],
            ["hosting", "Hosting"],
            ["training", "Training"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title
