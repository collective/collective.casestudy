"""Module where all interfaces, events and exceptions live."""
from collective.casestudy import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICaseStudyLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICaseStudySettings(Interface):

    industries = schema.List(
        title=_("Industries."),
        description=_(
            "help_industries", default="List of industries available for Case Studies"
        ),
        value_type=schema.TextLine(),
        default=[],
    )
