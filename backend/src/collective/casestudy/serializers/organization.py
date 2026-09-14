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

A provider whose listing is public -- ``listed`` or ``verified`` in
``provider_workflow`` -- is reported with the ``providerView`` layout. Volto
resolves a layout view before a content type view, so the frontend renders the
provider page for it and the plain organization page for everything else,
without anyone changing the layout stored on the object.

The base class is :class:`SerializeFolderToJson` rather than
:class:`SerializeToJson`: Organization is a ``Container``, and plone.restapi
would otherwise report ``is_folderish: false`` for it and drop ``items``.
"""

from collective.casestudy.content.case_study import CaseStudy
from collective.casestudy.content.organization import IOrganization
from collective.casestudy.content.organization import Organization
from collective.casestudy.querystring.query_index_modifiers import LISTED_STATES
from collective.casestudy.querystring.query_index_modifiers import PROVIDER_WORKFLOW
from collective.casestudy.utils.relations import case_studies_for_organization
from collective.multiworkflow.utils.workflow import parse_state
from collective.multiworkflow.utils.workflow import WORKFLOW_STATES
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


#: Layout reported for a provider whose listing is public. It names the
#: ``layoutViews`` entry the frontend registers for the provider page.
PROVIDER_LAYOUT = "providerView"


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

    def _is_provider(self, result: dict) -> bool:
        """Tell whether the organization is a provider with a public listing.

        Reads the serialization rather than the object. ``is_provider`` is only
        in it when the current user may read the provider fields, and
        ``workflow_states`` -- which `collective.multiworkflow` adds to every
        content serialization -- lists the state of each workflow of the chain
        as ``<workflow-id>|<state-id>``. ``provider_workflow`` joins the chain
        for providers only.

        :param result: The serialization built so far, ``workflow_states``
            included.
        :returns: ``True`` if the organization is flagged as a provider and its
            ``provider_workflow`` state is one of
            :data:`~collective.casestudy.querystring.query_index_modifiers.LISTED_STATES`.
        """
        if not result.get("is_provider"):
            return False
        states = dict(parse_state(value) for value in result.get(WORKFLOW_STATES, []))
        return states.get(PROVIDER_WORKFLOW) in LISTED_STATES

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
        :returns: The inherited representation, ``workflow_states`` included,
            plus ``case_studies``, with ``layout`` set to
            :data:`PROVIDER_LAYOUT` for a provider whose listing is public.
        """
        result = super().__call__(
            version=version,
            include_items=include_items,
            include_expansion=include_expansion,
        )
        result["case_studies"] = json_compatible(self.get_case_studies())
        if self._is_provider(result):
            result["layout"] = PROVIDER_LAYOUT
        return result
