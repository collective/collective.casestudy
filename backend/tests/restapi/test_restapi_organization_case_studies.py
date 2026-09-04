"""``case_studies`` as it reaches a REST API client.

The serializer looks its relations up with ``plone.api.relation.get``, which
filters by the ``View`` permission of the requesting user. That is the part
worth asserting over the wire rather than in an integration test: an anonymous
visitor must not learn about a case study that has not been published.
"""

from . import DEFAULT_PASSWORD
from copy import deepcopy
from plone import api
from plone.app.testing import SITE_OWNER_NAME

import pytest
import transaction


ORGANIZATION_PATH = "/company-1"


@pytest.fixture
def organization(portal):
    """The published organization created by the ``portal`` fixture."""
    return portal["company-1"]


@pytest.fixture
def add_case_study(portal, organization, case_studies_payload):
    """Return a helper relating a new case study to the organization.

    :returns: Callable taking the relationship name -- ``organizations`` or
        ``providers`` -- and whether to publish the case study.
    """

    def func(relationship: str, published: bool = True, index: int = 0):
        payload = deepcopy(case_studies_payload[index])
        with api.env.adopt_user(SITE_OWNER_NAME):
            content = api.content.create(container=portal, **payload)
            api.relation.create(
                source=content, target=organization, relationship=relationship
            )
            if published:
                api.content.transition(content, transition="publish")
        transaction.commit()
        return content

    return func


class TestOrganizationCaseStudies:
    def test_empty_by_default(self, anon_request):
        """An organization with no relations still reports both buckets."""
        response = anon_request.get(ORGANIZATION_PATH)
        assert response.status_code == 200
        assert response.json()["case_studies"] == {"provided": [], "received": []}

    @pytest.mark.parametrize(
        "relationship,bucket",
        [
            ("organizations", "received"),
            ("providers", "provided"),
        ],
    )
    def test_published_case_study_is_public(
        self, anon_request, add_case_study, relationship: str, bucket: str
    ):
        """A published case study reaches anonymous visitors."""
        case_study = add_case_study(relationship)
        data = anon_request.get(ORGANIZATION_PATH).json()
        assert [item["title"] for item in data["case_studies"][bucket]] == [
            case_study.title
        ]

    def test_private_case_study_hidden_from_anonymous(
        self, anon_request, add_case_study
    ):
        """An unpublished case study is not disclosed by the relation."""
        add_case_study("organizations", published=False)
        data = anon_request.get(ORGANIZATION_PATH).json()
        assert data["case_studies"]["received"] == []

    def test_private_case_study_visible_to_manager(
        self, manager_request, add_case_study
    ):
        """The same relation is reported to someone allowed to see it."""
        case_study = add_case_study("organizations", published=False)
        data = manager_request.get(ORGANIZATION_PATH).json()
        assert [item["title"] for item in data["case_studies"]["received"]] == [
            case_study.title
        ]

    def test_buckets_are_independent(self, anon_request, add_case_study):
        """Providing a case study and being its subject are different things."""
        provided = add_case_study("providers", index=0)
        received = add_case_study("organizations", index=1)
        data = anon_request.get(ORGANIZATION_PATH).json()
        assert [item["title"] for item in data["case_studies"]["provided"]] == [
            provided.title
        ]
        assert [item["title"] for item in data["case_studies"]["received"]] == [
            received.title
        ]

    @pytest.mark.parametrize(
        "credentials",
        [
            (),
            ("manager", DEFAULT_PASSWORD),
            ("reader", DEFAULT_PASSWORD),
        ],
    )
    def test_key_present_for_every_role(self, request_factory, credentials):
        """The key is part of the representation, not of a privileged view."""
        session = request_factory()
        session.auth = credentials
        response = session.get(ORGANIZATION_PATH)
        assert response.status_code == 200
        assert "case_studies" in response.json()

    def test_summary_entries_carry_social_links(self, anon_request, add_case_study):
        """Case study summaries come from the default serializer, not ours.

        ``social_links`` is added for Organization only, so a CaseStudy
        summary must not grow one.
        """
        add_case_study("organizations")
        data = anon_request.get(ORGANIZATION_PATH).json()
        entry = data["case_studies"]["received"][0]
        assert "social_links" not in entry
