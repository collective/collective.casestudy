"""Module where all interfaces, events and exceptions live.

The registry records this package owns are described once, here, as a schema.
The GenericSetup profile imports that schema -- see
``profiles/default/registry/collective.casestudy.interfaces.ICaseStudySettings.xml``
-- and the control panel renders its form from it, so a record added here is a
record the site knows about everywhere.

Every vocabulary record holds an **ordered list of terms**, each an object with
a ``token`` and a ``title``. Two properties of that shape earn it:

``ordered``
    The order in the record is the order a form offers the terms in, which for
    Plone versions is newest first and for the rest is editorial. A mapping
    would have worked -- a registry ``Dict`` does keep insertion order -- but
    it could never grow a third attribute without a second migration.

``structured``
    Until profile version 2100 a term was the string ``"token|title"``, split
    on the first ``|``. That put a parser in every vocabulary, made a title
    containing a pipe unrepresentable, and gave the frontend nothing better to
    render than a list of raw strings.
"""

from collective.casestudy import _
from plone.autoform import directives
from plone.schema.jsonfield import JSONField
from plone.supermodel import model
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import json


#: Name of the frontend widget these records are edited with. Registered by
#: the Volto add-on; a frontend without it falls back to the generic JSON
#: editor rather than failing.
TERMS_WIDGET = "vocabulary_terms"

#: JSON schema every vocabulary record validates against: an ordered array of
#: ``{"token": ..., "title": ...}``. ``additionalProperties`` is closed so a
#: typo in a hand-edited profile is refused at import rather than stored and
#: silently ignored.
TERMS_JSON_SCHEMA: str = json.dumps({
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "token": {"type": "string", "minLength": 1},
            "title": {"type": "string", "minLength": 1},
        },
        "required": ["token", "title"],
        "additionalProperties": False,
    },
})


class ICaseStudyLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


def _terms_field(title, description) -> JSONField:
    """Declare a vocabulary record.

    :param title: Field title, shown in the control panel.
    :param description: Field description.
    :returns: The field, validating against :data:`TERMS_JSON_SCHEMA`.
    """
    return JSONField(
        title=title,
        description=description,
        schema=TERMS_JSON_SCHEMA,
        required=False,
        default=[],
    )


class ICaseStudySettings(Interface):
    """Site-wide settings for case studies and the organizations behind them."""

    model.fieldset(
        "default",
        label=_("Plone"),
        fields=["usages", "versions"],
    )

    model.fieldset(
        "organization",
        label=_("Organization"),
        fields=["industries"],
    )

    model.fieldset(
        "provider",
        label=_("Provider"),
        fields=["services"],
    )

    industries = _terms_field(
        _("Industries"),
        _(
            "help_industries",
            default=(
                "Industries a Case Study can be filed under. The token is "
                "what gets stored on the content, so changing it orphans "
                "the content already using it; the title is free to change."
            ),
        ),
    )

    usages = _terms_field(
        _("Usage"),
        _(
            "help_usages",
            default="Categories of Plone usage a Case Study can be filed under.",
        ),
    )

    versions = _terms_field(
        _("Plone Versions."),
        _(
            "help_versions",
            default=(
                "Plone versions a Case Study can name. Ordered newest first, "
                "which is the order the form offers them in."
            ),
        ),
    )

    services = _terms_field(
        _("Provided Services"),
        _(
            "help_services",
            default="Services a provider can offer to their customers.",
        ),
    )

    organization_sizes = _terms_field(
        _("Organization sizes"),
        _(
            "help_organization_sizes",
            default=(
                "Size buckets an organization can choose from, ordered smallest first."
            ),
        ),
    )

    directives.widget("industries", frontendOptions={"widget": TERMS_WIDGET})
    directives.widget("usages", frontendOptions={"widget": TERMS_WIDGET})
    directives.widget("versions", frontendOptions={"widget": TERMS_WIDGET})
    directives.widget("services", frontendOptions={"widget": TERMS_WIDGET})
    directives.widget("organization_sizes", frontendOptions={"widget": TERMS_WIDGET})
