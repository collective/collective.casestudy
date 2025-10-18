from collective.casestudy import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IProviderExtras(model.Schema):

    rating = schema.Int(
        title=_("Rating"),
        description=_("Internal rating, between 1 and 5."),
        min=1,
        max=5,
        required=False,
    )
