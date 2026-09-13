"""Fixtures for the querystring tests."""

from . import CASE_STUDIES
from . import DOCUMENT
from . import PLAIN_ORGANIZATION
from . import PROVIDERS
from . import PUBLISHED
from collections.abc import Callable
from collections.abc import Generator
from copy import deepcopy
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFCore.indexing import processQueue
from Products.CMFPlone.Portal import PloneSite
from typing import Any

import pytest


@pytest.fixture(scope="class")
def portal(portal_class) -> Generator[PloneSite, None, None]:
    """Yield the class-scoped Plone site."""
    yield portal_class


def _create(
    container: PloneSite, payload: dict, transitions: list[str]
) -> DexterityContent:
    """Create one content item and walk it through its transitions.

    :param container: Where the content is created.
    :param payload: Creation payload for :func:`plone.api.content.create`.
    :param transitions: Transition ids to run, in order.
    :returns: The new content.
    """
    content = api.content.create(container=container, **payload)
    for transition in transitions:
        api.content.transition(obj=content, transition=transition)
    return content


@pytest.fixture(scope="class")
def contents(
    portal, case_studies_payload, providers_payload, organizations_payload
) -> dict[str, DexterityContent]:
    """Create the content every search in a test class runs against.

    :returns: Mapping of content id to content.
    """
    created: dict[str, DexterityContent] = {}
    with api.env.adopt_roles(["Manager"]):
        for content_id, transitions in CASE_STUDIES.items():
            payload = {
                **deepcopy(case_studies_payload[0]),
                "id": content_id,
                "title": content_id,
            }
            created[content_id] = _create(portal, payload, transitions)
        for content_id, transitions in PROVIDERS.items():
            payload = {
                **deepcopy(providers_payload[0]),
                "id": content_id,
                "title": content_id,
            }
            created[content_id] = _create(portal, payload, transitions)
        organization = {
            **deepcopy(organizations_payload[0]),
            "id": PLAIN_ORGANIZATION,
            "title": PLAIN_ORGANIZATION,
        }
        created[PLAIN_ORGANIZATION] = _create(portal, organization, [])
        document = {"type": "Document", "id": DOCUMENT, "title": DOCUMENT}
        created[DOCUMENT] = _create(portal, document, [])
        for content_id in PUBLISHED:
            api.content.transition(obj=created[content_id], transition="publish")
    processQueue()
    return created


@pytest.fixture
def search(portal) -> Callable[..., set[str]]:
    """Return a helper running querystring criteria through the query builder.

    Goes through the ``querybuilderresults`` view, the path a listing block and
    ``@querystring-search`` take, so the ``IParsedQueryIndexModifier``
    utilities are applied exactly as in a site.

    :returns: Callable taking ``(field, operation, value)`` criteria and
        returning the ids of the content found.
    """

    def func(*criteria: tuple[str, str, Any]) -> set[str]:
        query = [
            {"i": field, "o": operation, "v": value}
            for field, operation, value in criteria
        ]
        view = api.content.get_view(
            name="querybuilderresults", context=portal, request=portal.REQUEST
        )
        processQueue()
        with api.env.adopt_roles(["Manager"]):
            brains = view._makequery(query=query, brains=True)
            return {brain.getId for brain in brains}

    return func
