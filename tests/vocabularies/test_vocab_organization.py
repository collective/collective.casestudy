from collective.casestudy import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabOrganizationSize:

    name = f"{PACKAGE_NAME}.vocabulary.organization_size"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "me",
            "small",
            "medium",
            "large",
        ],
    )
    def test_token(self, token):
        assert token in [x for x in self.vocab.by_token]
