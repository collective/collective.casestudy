from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession

import pytest
import transaction


DEFAULT_PASSWORD = "averylongpasswordbutnotthatlong"


def _create_user_with_role(role: str, username: str = ""):
    role_lower = role.lower()
    username = username if username else role_lower
    return api.user.create(
        email=f"{username}@plone.org",
        username=username,
        password=DEFAULT_PASSWORD,
        roles=(
            "Member",
            role,
        ),
    )


def _create_provider(portal, payload):
    """Create a provider in the root of the portal."""
    return api.content.create(container=portal, **payload)


def _publish_content(content):
    """Publish a content."""
    api.content.transition(content, transition="publish")


@pytest.fixture()
def app(functional):
    return functional["app"]


@pytest.fixture()
def portal(functional, providers_payload):
    portal = functional["portal"]
    with api.env.adopt_user(SITE_OWNER_NAME):
        roles = ("Reader", "Contributor", "Editor", "Reviewer", "Manager")
        for role in roles:
            _create_user_with_role(role)
        # Create a second contributor
        _create_user_with_role("Contributor", "owner")
    with api.env.adopt_user("owner"):
        # Create provider
        content = _create_provider(portal, providers_payload[0])
    with api.env.adopt_user(SITE_OWNER_NAME):
        # Publish provider
        _publish_content(content)

    transaction.commit()
    return portal


@pytest.fixture()
def http_request(functional):
    return functional["request"]


@pytest.fixture()
def request_factory(portal):
    def factory():
        url = portal.absolute_url()
        api_session = RelativeSession(url)
        api_session.headers.update({"Accept": "application/json"})
        return api_session

    return factory


@pytest.fixture()
def anon_request(request_factory):
    return request_factory()


@pytest.fixture()
def manager_request(request_factory):
    request = request_factory()
    request.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
    yield request
    request.auth = ()


@pytest.fixture()
def reviewer_request(request_factory):
    request = request_factory()
    request.auth = ("reviewer", DEFAULT_PASSWORD)
    yield request
    request.auth = ()


@pytest.fixture()
def editor_request(request_factory):
    request = request_factory()
    request.auth = ("editor", DEFAULT_PASSWORD)
    yield request
    request.auth = ()


@pytest.fixture()
def contributor_request(request_factory):
    request = request_factory()
    request.auth = ("contributor", DEFAULT_PASSWORD)
    yield request
    request.auth = ()
