"""The Organization content type.

One type for every organization in the ecosystem, whether it is a Plone
user, a solution provider, or both. It supersedes the separate Provider
type, which is kept only so existing content still opens.
"""

from collective.casestudy import _
from plone.autoform.directives import read_permission
from plone.dexterity.content import Container
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


#: Permission guarding the organization profile fields on read.
READ_PERMISSION = "collective.casestudy.organization_info.view"

#: Permission guarding the organization profile fields on write.
WRITE_PERMISSION = "collective.casestudy.organization_info.edit"


class IOrganization(Schema):
    """An organization in the Plone ecosystem."""

    industry = schema.Choice(
        title=_("label_industry", default="Industry"),
        vocabulary="collective.casestudy.vocabulary.industries",
        required=True,
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
    read_permission(organization_size=READ_PERMISSION)


@implementer(IOrganization)
class Organization(Container):
    """An organization in the Plone ecosystem."""
