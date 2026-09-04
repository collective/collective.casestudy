from . import CASE_STUDIES
from . import ORGANIZATIONS
from . import PROVIDERS
from collections.abc import Generator
from collective.casestudy.testing import FUNCTIONAL_TESTING
from collective.casestudy.testing import INTEGRATION_TESTING
from copy import deepcopy
from plone import api
from Products.CMFPlone.Portal import PloneSite
from pytest_plone import fixtures_factory
from zope.component.hooks import site as site_wrapper

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)


@pytest.fixture(scope="class")
def case_studies_payload() -> list:
    """Payload to create a new Case Study."""
    return deepcopy(CASE_STUDIES)


@pytest.fixture
def case_studies(portal, case_studies_payload) -> dict:
    """Create case study content items."""
    response = {}
    with api.env.adopt_roles(["Manager"]):
        for data in case_studies_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture(scope="class")
def organizations_payload() -> list:
    """Payload to create two organizations that are not providers."""
    return deepcopy(ORGANIZATIONS)


@pytest.fixture
def organizations(portal, organizations_payload) -> dict:
    """Create organization content items."""
    response = {}
    with api.env.adopt_roles(["Manager"]):
        for data in organizations_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture(scope="class")
def providers_payload() -> list:
    """Payload to create two organizations that are also providers."""
    return deepcopy(PROVIDERS)


@pytest.fixture
def providers(portal, providers_payload) -> dict:
    """Create organization content items flagged as providers."""
    response = {}
    with api.env.adopt_roles(["Manager"]):
        for data in providers_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture(scope="class")
def portal_class(integration_class) -> Generator[PloneSite, None, None]:
    """Create a class-scoped fixture for the portal."""
    if hasattr(integration_class, "testSetUp"):
        integration_class.testSetUp()
    portal = integration_class["portal"]
    with site_wrapper(portal):
        yield portal
    if hasattr(integration_class, "testTearDown"):
        integration_class.testTearDown()
