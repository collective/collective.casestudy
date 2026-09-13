"""The 2000 -> 2100 upgrade: vocabulary records become term objects.

The step reads whatever a site actually stores, so the fixtures put the
records back into their pre-2100 state -- old field, old values -- rather than
feeding the handler a literal.
"""

from collective.casestudy.upgrades.v2100.vocabulary import RECORD_NAMES
from collective.casestudy.upgrades.v2100.vocabulary import upgrade_vocabulary_records
from plone import api
from plone.registry import field as pfield
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import pytest


@pytest.fixture
def legacy_record(portal):
    """Return a helper putting one record back into its pre-2100 state.

    :returns: Callable taking a record name and the list of legacy strings.
    """

    def func(name: str, value: list[str]) -> None:
        registry = getUtility(IRegistry)
        key = f"casestudy.{name}"
        registry.records[key].field = pfield.List(
            title=name,
            value_type=pfield.TextLine(title="term"),
            required=False,
        )
        registry[key] = value

    return func


@pytest.fixture
def read(portal):
    """Return a helper reading a record back."""

    def func(name: str):
        return api.portal.get_registry_record(f"casestudy.{name}")

    return func


class TestUpgradeVocabularyRecords:
    def test_converts_token_title_strings(self, legacy_record, read):
        legacy_record("industries", ["gov|Government", "edu|Education"])
        upgrade_vocabulary_records(None)
        assert read("industries") == [
            {"token": "gov", "title": "Government"},
            {"token": "edu", "title": "Education"},
        ]

    def test_keeps_the_stored_order(self, legacy_record, read):
        """Order is what the record is for; the upgrade must not sort."""
        legacy_record("usages", ["c|C", "a|A", "b|B"])
        upgrade_vocabulary_records(None)
        assert [e["token"] for e in read("usages")] == ["c", "a", "b"]

    def test_versions_gain_the_derived_title(self, legacy_record, read):
        """`versions` held bare tokens; the displayed title becomes data."""
        legacy_record("versions", ["6.2", "6.1"])
        upgrade_vocabulary_records(None)
        assert read("versions") == [
            {"token": "6.2", "title": "Plone 6.2"},
            {"token": "6.1", "title": "Plone 6.1"},
        ]

    def test_versions_keep_a_title_a_site_had_set(self, legacy_record, read):
        """A site that used token|title on versions is not overwritten."""
        legacy_record("versions", ["6.2|Plone 6.2 LTS"])
        upgrade_vocabulary_records(None)
        assert read("versions") == [{"token": "6.2", "title": "Plone 6.2 LTS"}]

    def test_drops_unusable_entries(self, legacy_record, read):
        legacy_record("services", ["design|Design", "|no-token", ""])
        upgrade_vocabulary_records(None)
        assert read("services") == [{"token": "design", "title": "Design"}]

    def test_terms_a_site_added_survive(self, legacy_record, read):
        """The step converts what is stored, not what this package ships."""
        legacy_record("industries", ["gov|Government", "coop|Cooperative"])
        upgrade_vocabulary_records(None)
        assert {e["token"] for e in read("industries")} == {"gov", "coop"}

    def test_every_record_is_converted(self, legacy_record, read):
        for name in RECORD_NAMES:
            legacy_record(name, ["a|A"])
        upgrade_vocabulary_records(None)
        for name in RECORD_NAMES:
            assert read(name) == [{"token": "a", "title": "A"}], name

    def test_is_idempotent(self, legacy_record, read):
        """Running it twice, or after the profile was reimported, is a no-op."""
        legacy_record("industries", ["gov|Government"])
        upgrade_vocabulary_records(None)
        once = read("industries")
        upgrade_vocabulary_records(None)
        assert read("industries") == once

    def test_result_validates_against_the_new_field(self, legacy_record, read):
        """What it writes has to survive the schema the profile registers."""
        from collective.casestudy.interfaces import ICaseStudySettings

        legacy_record("industries", ["gov|Government"])
        upgrade_vocabulary_records(None)
        ICaseStudySettings["industries"].validate(read("industries"))

    def test_record_names_match_the_schema(self):
        """Between them, converted and created must cover every record.

        A field added to the schema without a decision about this upgrade is
        a record that stays empty on every upgraded site.
        """
        from collective.casestudy.interfaces import ICaseStudySettings
        from collective.casestudy.upgrades.v2100.vocabulary import NEW_RECORD

        assert set(RECORD_NAMES) | {NEW_RECORD} == set(ICaseStudySettings.names())

    def test_seeds_the_new_size_record(self, legacy_record, read):
        """It never existed before 2100, so nothing converts into it."""
        legacy_record("industries", ["gov|Government"])
        upgrade_vocabulary_records(None)
        tokens = [entry["token"] for entry in read("organization_sizes")]
        assert tokens == ["me", "small", "medium", "large"]

    def test_does_not_overwrite_sizes_a_site_already_has(self, read):
        """Guarded, so re-running after an edit does not undo it."""
        from plone import api

        api.portal.set_registry_record(
            "casestudy.organization_sizes",
            [{"token": "solo", "title": "Just me"}],
        )
        upgrade_vocabulary_records(None)
        assert read("organization_sizes") == [{"token": "solo", "title": "Just me"}]
