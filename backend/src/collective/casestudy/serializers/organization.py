"""Serializers for the Organization content type.

An organization page has to show the case studies it takes part in, and there
are two ways to take part: an organization can be the *subject* of a case
study -- the ``organizations`` relation -- or it can have *delivered* one as a
solution provider -- the ``providers`` relation. Both relations point at the
organization, so neither is readable from the organization itself; they are
looked up in the relation catalog and folded into the serialization under
``case_studies``.

The lookup goes through :func:`plone.api.relation.get`, which drops broken
relations and filters by the ``View`` permission of the current user. An
anonymous visitor therefore never learns about an unpublished case study.

The base class is :class:`SerializeFolderToJson` rather than
:class:`SerializeToJson`: Organization is a ``Container``, and plone.restapi
would otherwise report ``is_folderish: false`` for it and drop ``items``.
"""

from collective.casestudy.content.case_study import CaseStudy
from collective.casestudy.content.organization import IOrganization
from collective.casestudy.content.organization import Organization
from collective.casestudy.utils.relations import case_studies_for_organization
from collective.multiworkflow import api as mw_api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest


def serialize_case_study(obj: CaseStudy, request: IBrowserRequest) -> dict:
    """Serialize a case study to its summary representation.

    A summary rather than the full object: an organization can be named by
    any number of case studies, and none of their blocks belong on its page.

    :param obj: The case study.
    :param request: Current request.
    :returns: The summary produced by :class:`ISerializeToJsonSummary`.
    """
    serializer = getMultiAdapter((obj, request), ISerializeToJsonSummary)
    return serializer()


@implementer(ISerializeToJsonSummary)
@adapter(IOrganization, Interface)
class OrganizationJSONSummarySerializer(DefaultJSONSummarySerializer):
    """Summary of an Organization, with its social links.

    A listing renders the logos of the networks an organization is on, and
    ``social_links`` is not a catalog column -- so a caller holding only the
    default summary would have to fetch the object to draw them.
    """

    def __call__(self) -> dict:
        """Build the summary.

        :returns: The default summary plus ``social_links``.
        """
        summary = super().__call__()
        summary["social_links"] = self.context.social_links
        return summary


@implementer(ISerializeToJson)
@adapter(IOrganization, Interface)
class OrganizationJSONSerializer(SerializeFolderToJson):
    """Full representation of an Organization, with its case studies."""

    context: Organization
    request: IBrowserRequest

    def get_case_studies(self) -> dict[str, list[dict]]:
        """Collect the case studies this organization takes part in.

        Both keys named by
        :data:`~collective.casestudy.utils.relations.RELATIONSHIPS` are
        always present, so a
        client never has to guard the lookup.

        :returns: Mapping of ``provided`` / ``received`` to lists of case
            study summaries.
        """
        raw_case_studies: dict[str, list[CaseStudy]] = case_studies_for_organization(
            self.context
        )
        case_studies: dict[str, list[dict]] = {}
        for key, contents in raw_case_studies.items():
            case_studies[key] = []
            for case_study in contents:
                case_studies[key].append(serialize_case_study(case_study, self.request))
        return case_studies

    def __call__(
        self,
        version: str | None = None,
        include_items: bool = True,
        include_expansion: bool = True,
    ) -> dict:
        """Serialize the organization.

        :param version: Version to serialize, or ``None`` for the current one.
        :param include_items: Whether to include the folder contents.
        :param include_expansion: Whether to run the registered expanders.
        :returns: The inherited representation plus ``case_studies`` and
            ``workflow_states``.
        """
        result = super().__call__(
            version=version,
            include_items=include_items,
            include_expansion=include_expansion,
        )
        workflow_states = mw_api.get_states(self.context)
        result.update(
            json_compatible({
                "case_studies": self.get_case_studies(),
                "workflow_states": workflow_states,
            })
        )
        return result
