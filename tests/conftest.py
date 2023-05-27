from collective.casestudy.testing import FUNCTIONAL_TESTING
from collective.casestudy.testing import INTEGRATION_TESTING
from plone import api
from pytest_plone import fixtures_factory

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (FUNCTIONAL_TESTING, "functional"),
            (INTEGRATION_TESTING, "integration"),
        )
    )
)


@pytest.fixture
def case_studies_payload() -> list:
    """Payload to create a new Case Study."""
    return [
        {
            "type": "CaseStudy",
            "title": "New Plone.org",
            "description": "An explanation about the new Plone.org",
            "subject": ["Tag 1", "Tag 2"],
            "industry": "ngo",
            "versions": [
                "6.0",
            ],
            "usages": [
                "portal",
            ],
            "remoteUrl": "https://plone.org",
            "id": "plone-org",
        },
        {
            "type": "CaseStudy",
            "title": "News Site",
            "description": "An explanation about the news site",
            "subject": ["Tag 1", "Tag 2"],
            "industry": "media",
            "versions": [
                "6.0",
            ],
            "usages": [
                "portal",
            ],
            "remoteUrl": "https://news-site.com",
            "id": "news-site",
        },
    ]


@pytest.fixture
def case_studies(portal, case_studies_payload) -> dict:
    """Create provider content items."""
    response = {}
    with api.env.adopt_roles(
        [
            "Manager",
        ]
    ):
        for data in case_studies_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture
def providers_payload() -> list:
    """Payload to create two providers."""
    return [
        {
            "type": "Provider",
            "id": "company-1",
            "title": "Company 1",
            "description": "A Plone Company provider",
            "remoteUrl": "https://company1.com",
            "country": "DE",
            "contact_name": "John Doe",
            "contact_email": "doe@company1.com",
            "contact_phone": "+4917632259823",
            "organization_size": "large",
            "services": [
                "design",
                "dev",
                "training",
            ],
        },
        {
            "type": "Provider",
            "id": "company-2",
            "title": "Company 2",
            "description": "Another Plone Company provider",
            "remoteUrl": "https://company2.com",
            "country": "CH",
            "contact_name": "Mary Jane",
            "contact_email": "mjane@company2.com",
            "contact_phone": "+4123632259823",
            "organization_size": "me",
            "services": [
                "hosting",
                "dev",
                "training",
            ],
        },
    ]


@pytest.fixture
def providers(portal, providers_payload) -> dict:
    """Create provider content items."""
    response = {}
    with api.env.adopt_roles(
        [
            "Manager",
        ]
    ):
        for data in providers_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response
