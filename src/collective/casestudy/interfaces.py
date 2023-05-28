"""Module where all interfaces, events and exceptions live."""
from collective.casestudy import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICaseStudyLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICaseStudySettings(Interface):

    industries = schema.List(
        title=_("Industries"),
        description=_(
            "help_industries",
            default=(
                "List of industries available for Case Studies in the "
                "format of `key|value`"
            ),
        ),
        value_type=schema.TextLine(),
        default=[],
    )

    usages = schema.List(
        title=_("Usage"),
        description=_(
            "help_usages",
            default=("Categories of Plone usage in the format of `key|value`"),
        ),
        value_type=schema.TextLine(),
        default=[],
    )

    versions = schema.List(
        title=_("Plone Versions."),
        description=_("help_versions", default="List of Plone Versions"),
        value_type=schema.TextLine(),
        default=[],
    )

    services = schema.List(
        title=_("Provided Services"),
        description=_(
            "help_services",
            default=(
                "List of services a provider offers to their customers in the "
                "format of `key|value`"
            ),
        ),
        value_type=schema.TextLine(),
        default=[],
    )
