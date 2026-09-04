"""Shared values for the collective.casestudy test suite.

Content payloads live here rather than in ``conftest.py`` so they can be
imported relatively from any test package: ``from tests import PROVIDERS``.
The fixtures that hand them out are in :mod:`tests.conftest`.
"""

#: Case studies created by the ``case_studies`` fixture.
CASE_STUDIES = [
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

#: Organizations that are plain Plone users, not providers.
#:
#: ``is_provider`` is deliberately left out so these exercise the schema
#: default: an organization is a Plone user until it opts in.
ORGANIZATIONS = [
    {
        "type": "Organization",
        "id": "ngo-1",
        "title": "NGO 1",
        "description": "A Plone user",
        "industry": "ngo",
        "country": "BR",
        "contact_name": "Joao Silva",
        "contact_email": "joao@ngo1.org",
        "contact_phone": "+551139496523",
        "organization_size": "small",
    },
    {
        "type": "Organization",
        "id": "ngo-2",
        "title": "NGO 2",
        "description": "Another Plone user",
        "industry": "ngo",
        "country": "AR",
        "contact_name": "Juan Martin",
        "contact_email": "juan@ngo2.org",
        "contact_phone": "+541139496523",
        "organization_size": "small",
    },
]

#: Organizations that are also solution providers.
PROVIDERS = [
    {
        "type": "Organization",
        "id": "company-1",
        "title": "Company 1",
        "description": "A Plone Company provider",
        "industry": "technology",
        "country": "DE",
        "contact_name": "John Doe",
        "contact_email": "doe@company1.com",
        "contact_phone": "+4917632259823",
        "organization_size": "large",
        "is_provider": True,
        "services": [
            "design",
            "dev",
            "training",
        ],
    },
    {
        "type": "Organization",
        "id": "company-2",
        "title": "Company 2",
        "description": "Another Plone Company provider",
        "industry": "technology",
        "country": "CH",
        "contact_name": "Mary Jane",
        "contact_email": "mjane@company2.com",
        "contact_phone": "+4123632259823",
        "organization_size": "me",
        "is_provider": True,
        "services": [
            "hosting",
            "dev",
            "training",
        ],
    },
]
