from collective.casestudy import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabIndustries:
    name = f"{PACKAGE_NAME}.vocabulary.industries"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "gov",
            "edu",
            "corporate",
            "media",
            "ngo",
        ],
    )
    def test_token(self, token):
        assert token in list(self.vocab.by_token)
