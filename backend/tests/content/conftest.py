from collections.abc import Callable
from collections.abc import Generator
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.Portal import PloneSite

import pytest


@pytest.fixture(scope="class")
def portal(portal_class) -> Generator[PloneSite, None, None]:
    """Yield the class-scoped Plone site."""
    yield portal_class


@pytest.fixture(scope="session")
def content_factory() -> Callable[[DexterityContent, dict], DexterityContent]:
    """Return a factory to create content inside a container.

    :returns: Callable taking a container and a creation payload -- keys
        starting with ``_`` are dropped -- and returning the new content.
    """

    def func(container: DexterityContent, payload: dict) -> DexterityContent:
        payload = {k: v for k, v in payload.items() if not k.startswith("_")}
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=container, **payload)
        return content

    return func


@pytest.fixture(scope="class")
def container(portal) -> DexterityContent:
    """Return the container used to create the content instance under test.

    :param portal: Plone site.
    :returns: Container for newly created content -- the portal, by default.
    """
    return portal


@pytest.fixture(scope="class")
def content_instance(
    content_factory: Callable[[DexterityContent, dict], DexterityContent],
    container: DexterityContent,
    payload: dict,
) -> Generator[DexterityContent, None, None]:
    """Create a content instance for the test class and remove it afterwards.

    :param content_factory: Factory returned by :func:`content_factory`.
    :param container: Container the content is created in.
    :param payload: Creation payload, provided by the test module.
    :returns: Generator yielding the new content object.
    """
    with api.env.adopt_roles(["Manager"]):
        content = content_factory(container, payload)
    content_id = content.id
    yield content
    # Cleanup after test
    with api.env.adopt_roles(["Manager"]):
        if content_id in container:
            container.manage_delObjects([content_id])
