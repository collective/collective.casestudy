from collective.casestudy import _
from collective.multiworkflow.interfaces import IAdditionalWorkflows
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider


#: Permission guarding the provider fields on read. Unlike contact
#: information these are public: a listing has to show them.
READ_PERMISSION = "collective.casestudy.provider_info.view"

#: Permission to edit the services a provider offers.
WRITE_PERMISSION = "collective.casestudy.provider_info.edit"

#: Permission to flag an organization as a provider. Separate from
#: :data:`WRITE_PERMISSION`: claiming provider status is a decision for
#: the site, not for the organization editing its own page.
MANAGE_PERMISSION = "collective.casestudy.provider_info.manage"


@provider(IFormFieldProvider)
class IProviderInfo(model.Schema):
    """A behavior with information about a solution provider."""

    directives.fieldset(
        "provider_info",
        label=_("label_provider_info", default="Provider Information"),
        fields=(
            "is_provider",
            "services",
        ),
    )
    is_provider = schema.Bool(
        title=_("label_is_provider", default="Is Provider"),
        description=_(
            "description_is_provider",
            default="Indicates if the organization is also a provider.",
        ),
        default=False,
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
    read_permission(is_provider=READ_PERMISSION, services=READ_PERMISSION)
    write_permission(is_provider=MANAGE_PERMISSION, services=WRITE_PERMISSION)


class IProvider(IAdditionalWorkflows):
    """Marker for content whose provider status is tracked."""
