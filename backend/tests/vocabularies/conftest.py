from collections.abc import Callable
from plone import api

import pytest


@pytest.fixture(scope="class")
def create_contents(portal_class) -> Callable[[list[dict]], dict]:
    """Return a helper to create content items in the class-scoped site.

    Dynamic vocabularies are built from the catalog, so their content has to
    live as long as the class-scoped portal the vocabulary is looked up on.

    :param portal_class: Class-scoped Plone site.
    :returns: Callable taking a list of creation payloads and returning a
        mapping of UID to title for the items created.
    """

    def func(payloads: list[dict]) -> dict:
        response = {}
        with api.env.adopt_roles(["Manager"]):
            for data in payloads:
                content = api.content.create(container=portal_class, **data)
                response[content.UID()] = content.title
        return response

    return func


@pytest.fixture
def reindex_organizations(portal_class) -> Callable[[], None]:
    """Return a helper reindexing every Organization in the site.

    Vocabularies built from ``uniqueValuesFor`` only see the first item
    created by a class-scoped fixture; reindexing from the test itself is
    what makes the whole index visible.

    :param portal_class: Class-scoped Plone site.
    :returns: Callable reindexing all Organization content.
    """

    def func() -> None:
        for brain in api.content.find(portal_type="Organization"):
            brain.getObject().reindexObject()

    return func


@pytest.fixture(scope="class")
def organizations_class(create_contents, organizations_payload) -> dict:
    """Create the plain organizations in the class-scoped site.

    :returns: Mapping of UID to title.
    """
    return create_contents(organizations_payload)


@pytest.fixture(scope="class")
def providers_class(create_contents, providers_payload) -> dict:
    """Create the provider organizations in the class-scoped site.

    :returns: Mapping of UID to title.
    """
    return create_contents(providers_payload)
