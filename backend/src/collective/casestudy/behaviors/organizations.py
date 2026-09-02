from collective.casestudy import _
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


@provider(IFormFieldProvider)
class IOrganizations(model.Schema):
    """Add a relation between a content item and one or more Organizations"""

    organizations = RelationList(
        title=_("label_organizations", default="Organizations"),
        description=_(
            "description_organizations",
            default="One or more organizations used in this case study",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("label_organization", default="Organization"),
            vocabulary=StaticCatalogVocabulary({
                "portal_type": ["Organization"],
            }),
        ),
    )
