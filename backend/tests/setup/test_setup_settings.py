"""The vocabulary settings records.

Each is an ordered array of ``{"token", "title"}``, declared once in
``ICaseStudySettings`` and shipped by the default profile.
"""

from collective.casestudy import PACKAGE_NAME
from collective.casestudy.interfaces import ICaseStudySettings
from collective.casestudy.interfaces import TERMS_WIDGET
from plone import api
from plone.autoform.interfaces import WIDGETS_KEY
from plone.restapi.types.interfaces import IJsonSchemaProvider
from plone.supermodel.utils import mergedTaggedValueDict
from zope.component import getMultiAdapter
from zope.schema.interfaces import WrongContainedType

import pytest


RECORDS = [
    "industries",
    "usages",
    "versions",
    "services",
    "organization_sizes",
]


@pytest.fixture
def record(portal):
    """Return a helper reading one of this package's settings records."""

    def func(name: str):
        return api.portal.get_registry_record(f"casestudy.{name}")

    return func


class TestSettingsSchema:
    """What the interface declares, before any site exists."""

    @pytest.mark.parametrize("name", RECORDS)
    def test_field_exists(self, name: str):
        assert name in ICaseStudySettings

    @pytest.mark.parametrize("name", RECORDS)
    def test_field_defaults_to_empty(self, name: str):
        assert ICaseStudySettings[name].default == []

    @pytest.mark.parametrize("name", RECORDS)
    def test_field_names_the_frontend_widget(self, name: str):
        """The Volto add-on registers a widget under this name."""
        widgets = mergedTaggedValueDict(ICaseStudySettings, WIDGETS_KEY)
        assert widgets[name].params["frontendOptions"] == {"widget": TERMS_WIDGET}


class TestSettingsJsonSchema:
    """What the control panel form actually receives.

    The contract with the Volto add-on, and the reason it is asserted here
    rather than assumed: plone.restapi passes autoform widget params straight
    through without knowing what ``frontendOptions`` means, and Volto's
    ``Field`` resolves it *before* the field's own ``widget``. Neither half
    names the other, so nothing but this test connects them.
    """

    @pytest.fixture
    def field_schema(self, portal, http_request):
        """Return a helper serializing one settings field for the frontend."""

        def func(name: str) -> dict:
            field = ICaseStudySettings[name].bind(portal)
            provider = getMultiAdapter(
                (field, portal, http_request), IJsonSchemaProvider
            )
            return provider.get_schema()

        return func

    @pytest.mark.parametrize("name", RECORDS)
    def test_names_the_widget_volto_resolves_first(self, field_schema, name: str):
        schema = field_schema(name)
        assert schema["widgetOptions"]["frontendOptions"]["widget"] == TERMS_WIDGET

    @pytest.mark.parametrize("name", RECORDS)
    def test_falls_back_to_the_json_editor(self, field_schema, name: str):
        """A frontend without the add-on still gets an editable field."""
        assert field_schema(name)["widget"] == "json"

    @pytest.mark.parametrize("name", RECORDS)
    def test_declares_the_jsonfield_factory(self, field_schema, name: str):
        assert field_schema(name)["factory"] == "JSONField"

    @pytest.mark.parametrize("name", RECORDS)
    def test_defaults_to_an_empty_list(self, field_schema, name: str):
        assert field_schema(name)["default"] == []

    def test_accepts_a_term(self):
        ICaseStudySettings["industries"].validate([{"token": "x", "title": "y"}])

    @pytest.mark.parametrize(
        "value,reason",
        [
            ([{"token": "x"}], "no title"),
            ([{"title": "y"}], "no token"),
            ([{"token": "", "title": "y"}], "empty token"),
            ([{"token": "x", "title": ""}], "empty title"),
            ([{"token": "x", "title": "y", "extra": 1}], "unknown key"),
            (["x|y"], "the pre-2100 string form"),
        ],
    )
    def test_rejects(self, value, reason: str):
        """A hand-edited profile is refused at import, not stored and ignored."""
        with pytest.raises(WrongContainedType):
            ICaseStudySettings["industries"].validate(value)


class TestSettingsProfile:
    """What the default profile actually installs."""

    @pytest.mark.parametrize("name", RECORDS)
    def test_record_installed(self, record, name: str):
        assert isinstance(record(name), list)

    @pytest.mark.parametrize("name", RECORDS)
    def test_record_is_not_empty(self, record, name: str):
        assert len(record(name)) > 0

    @pytest.mark.parametrize("name", RECORDS)
    def test_every_entry_is_a_term(self, record, name: str):
        for entry in record(name):
            assert set(entry) == {"token", "title"}
            assert entry["token"]
            assert entry["title"]

    @pytest.mark.parametrize("name", RECORDS)
    def test_tokens_are_unique(self, record, name: str):
        tokens = [entry["token"] for entry in record(name)]
        assert len(tokens) == len(set(tokens))

    def test_titles_may_contain_an_ampersand(self, record):
        """`&` is markup in XML and has to be escaped in the profile.

        An unescaped one does not fail the record -- it fails the whole
        profile import, and the site comes up half-installed.
        """
        titles = [entry["title"] for entry in record("industries")]
        assert any("&" in title for title in titles)

    def test_organization_sizes_are_smallest_first(self, record):
        tokens = [entry["token"] for entry in record("organization_sizes")]
        assert tokens == ["me", "small", "medium", "large"]

    def test_versions_are_newest_first(self, record):
        """Record order is offer order, and this one is deliberate."""
        tokens = [entry["token"] for entry in record("versions")]
        assert tokens[0] == "6.2"
        assert tokens[:3] == ["6.2", "6.1", "6.0"]

    def test_versions_carry_explicit_titles(self, record):
        """Titles used to be derived; from 2100 they are stored."""
        entries = {e["token"]: e["title"] for e in record("versions")}
        assert entries["6.2"] == "Plone 6.2"

    @pytest.mark.parametrize(
        "name,token,title",
        [
            ("industries", "gov", "Government & Public Sector"),
            ("industries", "ngo", "Non-Profit & NGO"),
            ("organization_sizes", "me", "Just me"),
            ("organization_sizes", "large", "More than 30 employees"),
            ("usages", "portal", "Portal"),
            ("services", "design", "Design / Theming"),
        ],
    )
    def test_shipped_terms(self, record, name: str, token: str, title: str):
        entries = {e["token"]: e["title"] for e in record(name)}
        assert entries[token] == title

    def test_titles_may_contain_the_old_separator(self, record):
        """A pipe in a title was unrepresentable before 2100.

        Nothing shipped uses one; the point is that the format no longer
        forbids it, so this asserts the record round-trips one.
        """
        key = "casestudy.industries"
        original = api.portal.get_registry_record(key)
        api.portal.set_registry_record(
            key, [{"token": "x", "title": "Design | Theming"}]
        )
        try:
            assert api.portal.get_registry_record(key)[0]["title"] == (
                "Design | Theming"
            )
        finally:
            api.portal.set_registry_record(key, original)


def test_package_name():
    """Guard the prefix the records are stored under."""
    assert PACKAGE_NAME == "collective.casestudy"
