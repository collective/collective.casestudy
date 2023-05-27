from collective.casestudy import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IAddressInfo(model.Schema):

    address = schema.TextLine(
        title=_("label_address", default="Company Address"), required=False
    )

    address_2 = schema.TextLine(
        title=_("label_address_2", default="Additional Info"),
        description=_("description_address_2", default="Example: Room 2"),
        required=False,
    )

    city = schema.TextLine(
        title=_("label_city", default="City"),
        description=_("description_city", default="Example: Brasília"),
        required=False,
    )

    state = schema.TextLine(
        title=_("label_state", default="State / Province"),
        description=_("description_state", default="DF"),
        required=False,
    )

    postal_code = schema.TextLine(
        title=_("label_postal_code", default="Postal Code"),
        description=_("description_postal_code", default="70123"),
        required=False,
    )

    country = schema.Choice(
        title=_("label_country", default="Country"),
        description=_(
            "description_country", default="Country where the provider is based"
        ),
        vocabulary="collective.casestudy.vocabulary.available_countries",
        required=True,
    )
