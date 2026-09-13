"""The ``@history`` endpoint on an organization running two workflows.

Core builds its listing from an untargeted ``review_history`` read, which
always resolves to the first workflow in the chain -- so a provider's
transitions would simply be absent. `collective.multiworkflow` overrides the
endpoint for participating content to merge them in and tag every entry with
the workflow that recorded it.

These are functional tests because the override is a ``plone:service``
registration, not something reachable from the object alone.
"""

from . import DEFAULT_PASSWORD
from plone import api
from plone.app.testing import SITE_OWNER_NAME

import pytest
import transaction


PUBLICATION_WORKFLOW = "simple_publication_workflow"
PROVIDER_WORKFLOW = "provider_workflow"


def workflow_entries(history: list, workflow_id: str) -> list:
    """Return the entries one workflow recorded.

    :param history: An ``@history`` listing.
    :param workflow_id: The workflow to filter on.
    :returns: That workflow's entries, in listing order.
    """
    return [entry for entry in history if entry.get("workflow_id") == workflow_id]


@pytest.fixture
def verified_provider(portal):
    """The published provider, moved through to ``verified``."""
    content = portal["company-1"]
    with api.env.adopt_user(SITE_OWNER_NAME):
        api.content.transition(obj=content, transition="verify")
    transaction.commit()
    return content


@pytest.fixture
def plain_organization(portal, organizations_payload):
    """An organization that never opted in to being a provider."""
    with api.env.adopt_user(SITE_OWNER_NAME):
        content = api.content.create(container=portal, **organizations_payload[0])
    transaction.commit()
    return content


@pytest.fixture
def history(request_factory, verified_provider) -> list:
    """The ``@history`` listing for a published, verified provider."""
    session = request_factory()
    session.auth = ("manager", DEFAULT_PASSWORD)
    response = session.get("/company-1/@history")
    assert response.status_code == 200
    return response.json()


class TestBothWorkflowsReachTheListing:
    def test_publication_entries_are_present(self, history):
        """The entries core already returned are tagged, not replaced."""
        assert workflow_entries(history, PUBLICATION_WORKFLOW)

    def test_provider_entries_are_present(self, history):
        """These are the ones an untargeted read would have dropped."""
        assert workflow_entries(history, PROVIDER_WORKFLOW)

    def test_the_verify_transition_is_listed(self, history):
        actions = [
            entry.get("action")
            for entry in workflow_entries(history, PROVIDER_WORKFLOW)
        ]
        assert "verify" in actions

    def test_the_publish_transition_is_still_listed(self, history):
        actions = [
            entry.get("action")
            for entry in workflow_entries(history, PUBLICATION_WORKFLOW)
        ]
        assert "publish" in actions


class TestEveryEntryIsAttributed:
    def test_all_entries_carry_the_key(self, history):
        """``workflow_id`` is unconditional, so clients can rely on it."""
        assert all("workflow_id" in entry for entry in history)

    def test_workflow_entries_name_their_workflow(self, history):
        for entry in history:
            if entry.get("type") == "workflow":
                assert entry["workflow_id"] is not None

    def test_no_entry_is_attributed_to_an_unknown_workflow(self, history):
        known = {PUBLICATION_WORKFLOW, PROVIDER_WORKFLOW, None}
        assert {entry.get("workflow_id") for entry in history} <= known


class TestPlainOrganizationIsUnaffected:
    def test_it_reports_only_publication(self, request_factory, plain_organization):
        """Content that never opted in keeps the stock payload's workflows."""
        session = request_factory()
        session.auth = ("manager", DEFAULT_PASSWORD)
        response = session.get(f"/{plain_organization.getId()}/@history")
        assert response.status_code == 200
        assert workflow_entries(response.json(), PROVIDER_WORKFLOW) == []
