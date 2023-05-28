from collective.casestudy import _
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


@provider(IFormFieldProvider)
class IProviders(model.Schema):

    providers = RelationList(
        title=_("label_providers", default="Providers"),
        description=_(
            "description_providers",
            default="One or more providers connected to this item",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("label_provider", default="Provider"),
            vocabulary=StaticCatalogVocabulary(
                {
                    "portal_type": ["Provider"],
                }
            ),
        ),
    )
