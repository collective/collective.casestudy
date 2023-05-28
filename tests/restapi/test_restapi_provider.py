from copy import deepcopy

import pytest


DEFAULT_PASSWORD = "averylongpasswordbutnotthatlong"


@pytest.fixture
def payload(providers_payload):
    # We use the second provider, as the first is already created
    payload = deepcopy(providers_payload[1])
    payload["@type"] = payload["type"]
    del payload["type"]
    return payload


@pytest.fixture
def provider(payload, contributor_request):
    response = contributor_request.post("/", json=payload)
    assert response.status_code == 201
    data = response.json()
    return data["id"]


class TestContentProviderPost:
    def test_manager_can_create(self, manager_request, payload):
        response = manager_request.post("/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, dict)
        assert data["id"] == "company-2"
        assert data["title"] == "Company 2"
        assert data["country"]["token"] == "CH"

    def test_contributor_can_create(self, contributor_request, payload):
        response = contributor_request.post("/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, dict)
        assert data["id"] == "company-2"
        assert data["title"] == "Company 2"
        assert data["country"]["token"] == "CH"

    def test_editor_cannot_create(self, editor_request, payload):
        response = editor_request.post("/", json=payload)
        assert response.status_code == 401

    def test_editor_can_view(self, editor_request, provider):
        response = editor_request.get(f"/{provider}")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "private"

    def test_contributor_can_ask_review(self, contributor_request, provider):
        response = contributor_request.post(f"/{provider}/@workflow/submit")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "pending"

    def test_reviewer_can_publish(
        self, contributor_request, reviewer_request, provider
    ):
        contributor_request.post(f"/{provider}/@workflow/submit")
        # Reviewer publish
        response = reviewer_request.post(f"/{provider}/@workflow/publish")
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
        """Check which roles can see contact information for a published provider.
        Use the provider created by the user "owner"."""
        session = request_factory()
        session.auth = credentials
        response = session.get("/company-1")
        assert response.status_code == 200
        data = response.json()
        assert data["review_state"] == "published"
        assert (
            "contact_name" in data
        ) is expected, f"Failed the check for {role} can view contact info"
