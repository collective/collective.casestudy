from collective.casestudy.behaviors.provider_info import IProviderInfo
from collective.casestudy.behaviors.provider_info import READ_PERMISSION
from collective.casestudy.behaviors.provider_info import WRITE_PERMISSION
from collective.casestudy.vocabularies.organization import DEFAULT_FACET
from collective.casestudy.vocabularies.organization import PROVIDER_FACET
from plone import api
from plone.app.textfield import RichText as RichTextField
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.widgets.richtext import RichTextFieldWidget
from plone.autoform.interfaces import READ_PERMISSIONS_KEY
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.rfc822.interfaces import IPrimaryField
from plone.supermodel.interfaces import FIELDSETS_KEY

import pytest


BEHAVIOR = "collective.casestudy.provider_info"
CONTENT_TYPE = "Organization"


class TestProviderInfoBehavior:
    def test_behavior_enabled(self, integration, get_behaviors):
        assert BEHAVIOR in get_behaviors(CONTENT_TYPE)

    def test_is_provider_defaults_to_false(self, portal, organizations_payload):
        """An organization is a Plone user until it opts in as a provider."""
        payload = organizations_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)
        assert content.is_provider is False

    def test_facets_of_plain_organization(self, portal, organizations):
        """A plain organization carries the default facet, never the provider one."""
        for uid in organizations:
            brain = api.content.find(UID=uid)[0]
            assert brain.facets == [DEFAULT_FACET]

    def test_facets_of_provider(self, portal, providers):
        for uid in providers:
            brain = api.content.find(UID=uid)[0]
            assert DEFAULT_FACET in brain.facets
            assert PROVIDER_FACET in brain.facets

    @pytest.mark.parametrize(
        "facet,expected",
        [
            (DEFAULT_FACET, 2),
            (PROVIDER_FACET, 0),
        ],
    )
    def test_facets_index(self, portal, organizations, facet, expected):
        brains = api.content.find(portal_type=CONTENT_TYPE, facets=facet)
        assert len(brains) == expected

    def test_services_indexed(self, portal, providers):
        brains = api.content.find(services="hosting")
        assert len(brains) == 1
        assert brains[0].Title == "Company 2"


class TestProviderText:
    """The ``text`` field, set up like ``plone.app.contenttypes``' richtext."""

    def test_it_is_rich_text(self):
        assert isinstance(IProviderInfo["text"], RichTextField)

    def test_it_is_optional(self):
        assert IProviderInfo["text"].required is False

    def test_it_uses_the_rich_text_widget(self):
        """The directive may store the factory itself or wrap it."""
        registered = IProviderInfo.queryTaggedValue(WIDGETS_KEY)["text"]
        factory = getattr(registered, "widget_factory", registered)
        assert factory is RichTextFieldWidget

    def test_it_is_the_primary_field(self):
        assert IPrimaryField.providedBy(IProviderInfo["text"])

    def test_it_is_in_the_provider_fieldset(self):
        fieldsets = IProviderInfo.queryTaggedValue(FIELDSETS_KEY)
        fields = {fieldset.__name__: fieldset.fields for fieldset in fieldsets}[
            "provider_info"
        ]
        assert "text" in fields

    def test_it_is_read_like_services(self):
        """Public once the listing is, through ``provider_workflow``."""
        permissions = IProviderInfo.queryTaggedValue(READ_PERMISSIONS_KEY)
        assert permissions["text"] == READ_PERMISSION

    def test_it_is_written_like_services(self):
        """The organization edits it, unlike ``is_provider``."""
        permissions = IProviderInfo.queryTaggedValue(WRITE_PERMISSIONS_KEY)
        assert permissions["text"] == WRITE_PERMISSION

    def test_it_defaults_to_empty(self, portal, providers_payload):
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **providers_payload[0])
        assert content.text is None

    def test_it_stores_rich_text(self, portal, providers_payload):
        payload = {
            **providers_payload[0],
            "text": RichTextValue("<p>We build Plone sites.</p>", "text/html"),
        }
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=portal, **payload)
        assert content.text.raw == "<p>We build Plone sites.</p>"
