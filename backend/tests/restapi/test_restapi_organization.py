from . import DEFAULT_PASSWORD
from copy import deepcopy
from plone import api
from plone.app.testing import SITE_OWNER_NAME

import pytest
import transaction


@pytest.fixture
def payload(providers_payload):
    # We use the second organization, as the first is already created
    payload = deepcopy(providers_payload[1])
    payload["@type"] = payload["type"]
    del payload["type"]
    return payload


@pytest.fixture
def organization(payload, contributor_request):
    response = contributor_request.post("/", json=payload)
    assert response.status_code == 201
    data = response.json()
    return data["id"]


@pytest.fixture
def verified_provider(portal):
    """Move the published provider through to ``verified``.

    ``verify`` is a transition of ``provider_workflow``, the chain entry the
    ``IProvider`` marker adds -- it does not touch the publication state.
    """
    content = portal["company-1"]
    with api.env.adopt_user(SITE_OWNER_NAME):
        api.content.transition(obj=content, transition="verify")
    transaction.commit()
    return content


class TestContentOrganizationPost:
    def test_manager_can_create(self, manager_request, payload):
        response = manager_request.post("/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, dict)
        assert data["@type"] == "Organization"
        assert data["id"] == "company-2"
        assert data["title"] == "Company 2"
        assert data["country"]["token"] == "CH"  # noQA: S105

    def test_contributor_can_create(self, contributor_request, payload):
        response = contributor_request.post("/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, dict)
        assert data["@type"] == "Organization"
        assert data["id"] == "company-2"
        assert data["title"] == "Company 2"
        assert data["country"]["token"] == "CH"  # noQA: S105

    def test_editor_cannot_create(self, editor_request, payload):
        response = editor_request.post("/", json=payload)
        assert response.status_code == 401

    def test_editor_can_view(self, editor_request, organization):
        response = editor_request.get(f"/{organization}")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "private"

    def test_contributor_can_ask_review(self, contributor_request, organization):
        response = contributor_request.post(f"/{organization}/@workflow/submit")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "pending"

    def test_reviewer_can_publish(
        self, contributor_request, reviewer_request, organization
    ):
        contributor_request.post(f"/{organization}/@workflow/submit")
        # Reviewer publish
        response = reviewer_request.post(f"/{organization}/@workflow/publish")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "published"

    @pytest.mark.parametrize(
        "role,credentials,expected",
        [
            ["Manager", ("manager", DEFAULT_PASSWORD), True],
            ["Editor", ("editor", DEFAULT_PASSWORD), True],
            ["Reviewer", ("reviewer", DEFAULT_PASSWORD), True],
            ["Owner", ("owner", DEFAULT_PASSWORD), True],
            ["Reader", ("reader", DEFAULT_PASSWORD), False],
            ["Contributor", ("contributor", DEFAULT_PASSWORD), False],
            ["Anonymous", (), False],
        ],
    )
    def test_role_can_view_contact_info(
        self, request_factory, role, credentials, expected
    ):
        """Check which roles can see contact information for a published organization.

        This is enforced by the acquired ``View Contact Information`` grants
        in the rolemap, not by a per-state permission map.

        Use the organization created by the user "owner".
        """
        session = request_factory()
        session.auth = credentials
        response = session.get("/company-1")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "published"
        assert ("contact_name" in data) is expected, (
            f"Failed the check for {role} can view contact info"
        )

    @pytest.mark.parametrize(
        "role,credentials,expected",
        [
            ["Manager", ("manager", DEFAULT_PASSWORD), True],
            ["Editor", ("editor", DEFAULT_PASSWORD), True],
            ["Anonymous", (), False],
        ],
    )
    def test_role_can_view_provider_info_before_listing(
        self, request_factory, role, credentials, expected
    ):
        """Provider information is staff-only until the listing is approved.

        The organization is *published* -- the page itself is public -- but
        ``provider_workflow`` starts in ``created``, whose permission map is
        not acquired and does not name Anonymous. Publishing the page and
        listing the provider are separate decisions.
        """
        session = request_factory()
        session.auth = credentials
        response = session.get("/company-1")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "published"
        assert ("services" in data) is expected, (
            f"Failed the check for {role} can view provider info"
        )

    @pytest.mark.parametrize(
        "role,credentials,expected",
        [
            ["Manager", ("manager", DEFAULT_PASSWORD), True],
            ["Editor", ("editor", DEFAULT_PASSWORD), True],
            ["Anonymous", (), True],
        ],
    )
    def test_role_can_view_provider_info_once_verified(
        self, request_factory, verified_provider, role, credentials, expected
    ):
        """Once verified, provider information is public."""
        session = request_factory()
        session.auth = credentials
        response = session.get("/company-1")
        assert response.status_code == 200
        data = response.json()
        assert data["workflow_states"]["provider_workflow"] == "verified"
        assert ("services" in data) is expected, (
            f"Failed the check for {role} can view provider info"
        )
