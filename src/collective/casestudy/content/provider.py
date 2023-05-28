from collective.casestudy import _
from plone.autoform.directives import read_permission
from plone.dexterity.content import Container
from plone.supermodel import directives
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


PERMISSION = "collective.casestudy.organization_info.view"


class IProvider(Schema):
    """A Plone Solution Provider of Plone usage."""

    remoteUrl = schema.TextLine(
        title=_("label_site", default="Company site"),
    )
    services = schema.List(
        title=_("label_services", default="Services"),
        description=_(
            "description_services",
            default="List of services you provide",
        ),
        value_type=schema.Choice(
            vocabulary="collective.casestudy.vocabulary.services",
        ),
        default=[],
        required=False,
    )

    read_permission(organization_size=PERMISSION)
    directives.fieldset(
        "organization",
        label=_("label_organization", default="Organization Information"),
        fields=("organization_size",),
    )
    organization_size = schema.Choice(
        title=_("label_organization_size", default="Organization size"),
        description=_(
            "description_organization_size",
            default="Estimated number of people in your organization",
        ),
        vocabulary="collective.casestudy.vocabulary.organization_size",
        required=True,
    )


@implementer(IProvider)
class Provider(Container):
    """A Plone Solution Provider of Plone usage."""
