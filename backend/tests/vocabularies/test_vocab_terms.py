"""Reading a settings record as vocabulary terms.

The shared builder behind the four vocabulary factories, including the
tolerance that keeps a site working between installing 2100 and running its
upgrade step.
"""

from collective.casestudy import PACKAGE_NAME
from collective.casestudy.vocabularies.terms import term_from_record
from collective.casestudy.vocabularies.terms import vocabulary_from_record
from plone import api
from plone.registry import field as pfield
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestTermFromRecord:
    """One entry, in any shape a site might hold."""

    @pytest.mark.parametrize(
        "entry,expected",
        [
            ({"token": "gov", "title": "Government"}, ("gov", "Government")),
            # Pre-2100 forms, still readable so an unmigrated site works.
            ("gov|Government", ("gov", "Government")),
            ("6.2", ("6.2", "6.2")),
            # Only the first separator splits, so a title may contain one.
            ("x|Design | Theming", ("x", "Design | Theming")),
            # A stored object with no title falls back to the token.
            ({"token": "gov"}, ("gov", "gov")),
            ({"token": "gov", "title": ""}, ("gov", "gov")),
        ],
    )
    def test_readable(self, entry, expected):
        assert term_from_record(entry) == expected

    @pytest.mark.parametrize(
        "entry",
        [
            {},
            {"title": "Government"},
            {"token": ""},
            "",
            "|Government",
            None,
            42,
            ["gov", "Government"],
        ],
    )
    def test_unusable(self, entry):
        """Anything without a token is dropped rather than guessed at."""
        assert term_from_record(entry) is None


class TestVocabularyFromRecord:
    """The whole record."""

    @pytest.fixture
    def build(self, portal):
        """Return a helper writing a record and building its vocabulary."""

        def func(value) -> SimpleVocabulary:
            api.portal.set_registry_record("casestudy.industries", value)
            return vocabulary_from_record("industries")

        return func

    @pytest.fixture
    def build_legacy(self, portal):
        """Return a helper that stores a *pre-2100* record and reads it back.

        The 2100 field refuses the old shape, so the only way a site holds it
        is the way a real one does: values written while the record still
        carried the old ``List(TextLine)`` field, read after the interface was
        re-registered. Swapping the field back reproduces exactly that.
        """

        def func(value) -> SimpleVocabulary:
            registry = getUtility(IRegistry)
            key = "casestudy.industries"
            record = registry.records[key]
            record.field = pfield.List(
                title="Industries",
                value_type=pfield.TextLine(title="term"),
                required=False,
            )
            registry[key] = value
            return vocabulary_from_record("industries")

        return func

    def test_builds_from_the_current_shape(self, build):
        vocab = build([{"token": "gov", "title": "Government"}])
        term = vocab.getTermByToken("gov")
        assert term.title == "Government"
        assert term.value == "gov"

    def test_keeps_record_order(self, build):
        """Record order is offer order; a mapping would have sorted these."""
        vocab = build([
            {"token": "c", "title": "C"},
            {"token": "a", "title": "A"},
            {"token": "b", "title": "B"},
        ])
        assert [term.token for term in vocab] == ["c", "a", "b"]

    def test_empty_record(self, build):
        assert list(build([])) == []

    def test_reads_the_pre_2100_shape(self, build_legacy):
        """A site that has not run the upgrade still gets a working form."""
        vocab = build_legacy(["gov|Government", "edu|Education"])
        assert [term.token for term in vocab] == ["gov", "edu"]
        assert vocab.getTermByToken("gov").title == "Government"

    def test_reads_a_pre_2100_bare_token(self, build_legacy):
        """`versions` entries carried no title at all."""
        vocab = build_legacy(["6.2"])
        assert vocab.getTermByToken("6.2").title == "6.2"

    def test_drops_unusable_entries(self, build_legacy):
        vocab = build_legacy(["gov|Government", "|no-token"])
        assert [term.token for term in vocab] == ["gov"]

    def test_logs_what_it_drops(self, build_legacy, caplog):
        """Silently skipping would hide the data problem for good."""
        with caplog.at_level("WARNING", logger=PACKAGE_NAME):
            build_legacy(["|no-token"])
        assert "casestudy.industries" in caplog.text
