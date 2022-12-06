from collective.casestudy import _
from plone.dexterity.content import Container
from plone.supermodel.model import Schema
from zope.interface import implementer
from zope.schema import Choice
from zope.schema import TextLine


class ICaseStudy(Schema):
    """A case study of Plone usage."""

    industry = Choice(
        title=_("label_industry", default="Industry"),
        vocabulary="collective.casestudy.vocabulary.industries",
        required=True,
    )

    remoteUrl = TextLine(
        title=_("label_url", default="URL"),
    )


@implementer(ICaseStudy)
class CaseStudy(Container):
    """A case study of Plone usage."""
