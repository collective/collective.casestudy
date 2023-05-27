from collective.casestudy import _
from plone.autoform.directives import read_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.schema.email import Email
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider


PERMISSION = "collective.casestudy.contact_info.view"


@provider(IFormFieldProvider)
class IContactInfo(model.Schema):

    directives.fieldset(
        "contact_info",
        label=_("label_contact_info", default="Contact Information"),
        fields=("contact_name", "contact_email", "contact_phone"),
    )

    read_permission(
        contact_name=PERMISSION, contact_email=PERMISSION, contact_phone=PERMISSION
    )
    contact_name = schema.TextLine(
        title=_("label_contact_name", default="Contact Person"), required=True
    )

    contact_email = Email(
        title=_("label_contact_email", default="Contact Email"), required=True
    )

    contact_phone = schema.TextLine(
        title=_("label_contact_phone", default="Contact Phone Number"),
        description=_(
            "description_contact_phone",
            default=("Internationalized phone number with country code and area code"),
        ),
        required=True,
    )
