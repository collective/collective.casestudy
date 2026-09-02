from collective.casestudy import PACKAGE_NAME
from plone import api
from plone.app.vocabularies import SimpleTerm
from plone.app.vocabularies import SimpleVocabulary
from Products.CMFCore.indexing import processQueue

import pytest


class TestVocabAvailableCountries:
    """Every country pycountry knows about is offered on the address form."""

    name: str = f"{PACKAGE_NAME}.vocabulary.available_countries"
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
            ("BR", "Brazil"),
            ("GB", "United Kingdom"),
            ("RO", "Romania"),
            ("US", "United States"),
            ("ES", "Spain"),
            ("JP", "Japan"),
            ("IT", "Italy"),
            ("BE", "Belgium"),
        ],
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert isinstance(term, SimpleTerm)
        assert term.title == title
        assert term.token == token


class TestVocabCountries:
    """Only countries already used by an organization are listed."""

    name: str = f"{PACKAGE_NAME}.vocabulary.countries"
    vocab_type = SimpleVocabulary

    @pytest.fixture(autouse=True)
    def _setup(
        self, portal_class, get_vocabulary, providers_class, reindex_organizations
    ):
        self.portal = portal_class
        self.providers = providers_class
        reindex_organizations()
        self.vocab = get_vocabulary(self.name, self.portal)

    def test_vocabulary_type(self):
        assert isinstance(self.vocab, self.vocab_type)

    @pytest.mark.parametrize(
        "token,title",
        [
            ("CH", "Switzerland"),
            ("DE", "Germany"),
        ],
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert isinstance(term, SimpleTerm)
        assert term.title == title
        assert term.token == token

    @pytest.mark.parametrize(
        "token",
        [
            "BR",
            "ES",
        ],
    )
    def test_unused_country_not_in_vocab(self, token: str):
        assert token not in list(self.vocab.by_token)


class TestVocabCountriesWithUnknownCode:
    """A code the index holds but pycountry does not know.

    Reachable without anyone doing anything wrong: ISO retires alpha-2 codes,
    so content catalogued years ago can hold one pycountry no longer resolves.
    The vocabulary is looked up by every listing and every edit form, so it
    has to degrade rather than raise.
    """

    name: str = f"{PACKAGE_NAME}.vocabulary.countries"

    UNKNOWN_CODE: str = "XX"

    @pytest.fixture
    def portal_with_unknown_code(
        self, portal, organizations_payload, providers_payload
    ):
        """A site holding one known country code and one unknown one."""
        with api.env.adopt_roles(["Manager"]):
            api.content.create(container=portal, **providers_payload[0])
            unknown = api.content.create(container=portal, **organizations_payload[0])
        # Written straight onto the object: the field vocabulary would refuse
        # it today, which is the whole point -- it did not, once.
        unknown.country = self.UNKNOWN_CODE
        unknown.reindexObject(idxs=["country"])
        # CMFCore queues index operations and only applies them at the
        # transaction boundary, so without this the index still holds the
        # value the object was created with -- or nothing at all.
        processQueue()
        return portal

    @pytest.fixture
    def vocab(self, portal_with_unknown_code, get_vocabulary):
        return get_vocabulary(self.name, portal_with_unknown_code)

    def test_vocabulary_is_built(self, vocab):
        """The lookup succeeds instead of raising."""
        assert isinstance(vocab, SimpleVocabulary)

    def test_unknown_code_is_skipped(self, vocab):
        assert self.UNKNOWN_CODE not in list(vocab.by_token)

    def test_known_code_is_still_offered(self, vocab):
        """One bad value must not cost the rest of the vocabulary."""
        term = vocab.getTermByToken("DE")
        assert isinstance(term, SimpleTerm)
        assert term.title == "Germany"

    def test_index_really_holds_the_unknown_code(self, portal_with_unknown_code):
        """Guard the fixture itself, so the test above cannot pass vacuously."""
        catalog = api.portal.get_tool("portal_catalog")
        assert self.UNKNOWN_CODE in catalog.uniqueValuesFor("country")

    def test_unknown_code_is_logged(
        self, portal_with_unknown_code, get_vocabulary, caplog
    ):
        """Silently dropping it would hide the data problem for good."""
        with caplog.at_level("WARNING", logger=PACKAGE_NAME):
            get_vocabulary(self.name, portal_with_unknown_code)
        assert self.UNKNOWN_CODE in caplog.text
