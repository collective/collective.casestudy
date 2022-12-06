from collective.casestudy import _
from plone.dexterity.content import Container
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


class ICaseStudy(Schema):
    """A case study of Plone usage."""

    remoteUrl = schema.TextLine(
        title=_("label_url", default="URL"),
    )

    industry = schema.Choice(
        title=_("label_industry", default="Industry"),
        vocabulary="collective.casestudy.vocabulary.industries",
        required=True,
    )

    usages = schema.List(
        title=_("label_usages", default="Usages"),
        value_type=schema.Choice(
            vocabulary="collective.casestudy.vocabulary.usages",
        ),
        default=[],
        required=False,
    )

    versions = schema.List(
        title=_("label_versions", default="Versions"),
        value_type=schema.Choice(
            vocabulary="collective.casestudy.vocabulary.versions",
        ),
        default=[],
        required=False,
    )


@implementer(ICaseStudy)
class CaseStudy(Container):
    """A case study of Plone usage."""
