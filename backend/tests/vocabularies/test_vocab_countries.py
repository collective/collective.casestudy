from collective.casestudy import COUNTRIES_DOMAIN
from collective.casestudy import PACKAGE_NAME
from plone import api
from plone.app.vocabularies import SimpleTerm
from plone.app.vocabularies import SimpleVocabulary
from Products.CMFCore.indexing import processQueue
from zope.i18n import translate

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

    def test_titles_use_the_countries_domain(self):
        term = self.vocab.getTermByToken("BR")
        assert term.title.domain == COUNTRIES_DOMAIN

    @pytest.mark.parametrize(
        "token,language,expected",
        [
            ("BR", "pt_BR", "Brasil"),
            ("DE", "pt_BR", "Alemanha"),
            ("US", "es", "Estados Unidos"),
            ("DE", "es", "Alemania"),
            # Spelled the same in Portuguese: an empty msgstr falls back to it.
            ("PT", "pt_BR", "Portugal"),
        ],
    )
    def test_titles_are_translated(self, token: str, language: str, expected: str):
        term = self.vocab.getTermByToken(token)
        assert translate(term.title, target_language=language) == expected

    @pytest.fixture
    def vocab_in(self, get_vocabulary):
        """Build the vocabulary with the request negotiated to a language."""
        request = api.env.getRequest()
        original = request.get("LANGUAGE")

        def func(language: str) -> SimpleVocabulary:
            request["LANGUAGE"] = language
            return get_vocabulary(self.name, self.portal)

        yield func
        request["LANGUAGE"] = original

    @pytest.mark.parametrize(
        "language,first",
        [
            # "Åland Islands" right after "Afghanistan": accents are ignored.
            ("en", ["AF", "AX", "AL", "DZ", "AS"]),
            # "África do Sul" (ZA) between "Afeganistão" and "Albânia".
            ("pt_BR", ["AF", "ZA", "AL", "DE", "AD"]),
            ("es", ["AF", "AL", "DE", "DZ", "AD"]),
        ],
    )
    def test_sorted_by_translated_title(self, vocab_in, language: str, first: list):
        vocab = vocab_in(language)
        assert [term.token for term in vocab][:5] == first
        assert [term.token for term in vocab][-2:] == ["ZM", "ZW"]


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

    def test_sorted_by_title_not_by_code(self):
        """The index hands codes back in code order: CH before DE."""
        assert [term.token for term in self.vocab] == ["DE", "CH"]


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
