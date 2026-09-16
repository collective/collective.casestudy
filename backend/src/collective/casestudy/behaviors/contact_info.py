from collective.casestudy import _
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.schema.email import Email
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider


#: Permission guarding the contact fields on read. Contact details are
#: personal data, so they are not part of the public representation.
READ_PERMISSION = "collective.casestudy.contact_info.view"

#: Permission guarding the contact fields on write.
WRITE_PERMISSION = "collective.casestudy.contact_info.edit"


@provider(IFormFieldProvider)
class IContactInfo(model.Schema):
    directives.fieldset(
        "contact_info",
        label=_("label_contact_info", default="Contact Information"),
        fields=("contact_name", "contact_email", "contact_phone"),
    )

    contact_name = schema.TextLine(
        title=_("label_contact_name", default="Contact Person"), required=False
    )

    contact_email = Email(
        title=_("label_contact_email", default="Contact Email"), required=False
    )

    contact_phone = schema.TextLine(
        title=_("label_contact_phone", default="Contact Phone Number"),
        description=_(
            "description_contact_phone",
            default=("Internationalized phone number with country code and area code"),
        ),
        required=False,
    )

    read_permission(
        contact_name=READ_PERMISSION,
        contact_email=READ_PERMISSION,
        contact_phone=READ_PERMISSION,
    )
    write_permission(
        contact_name=WRITE_PERMISSION,
        contact_email=WRITE_PERMISSION,
        contact_phone=WRITE_PERMISSION,
    )
