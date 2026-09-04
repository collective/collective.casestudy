from collections.abc import Callable
from plone import api
from plone.dexterity.content import DexterityContent
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from Products.CMFPlone.Portal import PloneSite
from zope.component import getMultiAdapter
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.browser import IBrowserRequest

import pytest


@pytest.fixture
def create_one(portal: PloneSite) -> Callable[[dict], DexterityContent]:
    """Return a helper creating a single content item in the site root.

    :param portal: Plone site.
    :returns: Callable taking a creation payload and returning the content.
    """

    def func(payload: dict) -> DexterityContent:
        with api.env.adopt_roles(["Manager"]):
            return api.content.create(container=portal, **payload)

    return func


@pytest.fixture
def organization(create_one, organizations_payload) -> DexterityContent:
    """An organization that is a plain Plone user."""
    return create_one(organizations_payload[0])


@pytest.fixture
def provider(create_one, providers_payload) -> DexterityContent:
    """An organization that is also a solution provider."""
    return create_one(providers_payload[0])


@pytest.fixture
def case_study(create_one, case_studies_payload) -> DexterityContent:
    """A case study, unrelated to any organization."""
    return create_one(case_studies_payload[0])


@pytest.fixture
def other_case_study(create_one, case_studies_payload) -> DexterityContent:
    """A second case study, so relation filtering is observable."""
    return create_one(case_studies_payload[1])


@pytest.fixture
def relate() -> Callable[[DexterityContent, DexterityContent, str], None]:
    """Return a helper creating a relation between two content items.

    :returns: Callable taking source, target and the relationship name.
    """

    def func(source: DexterityContent, target: DexterityContent, name: str) -> None:
        api.relation.create(source=source, target=target, relationship=name)

    return func


@pytest.fixture
def serialize(
    http_request: IBrowserRequest,
) -> Callable[[DexterityContent, IInterface], dict]:
    """Return a helper running a content item through a serializer.

    :param http_request: Request the serializer is looked up on.
    :returns: Callable taking the object and, optionally, the serializer
        interface -- :class:`ISerializeToJson` by default.
    """

    def func(obj, iface: IInterface = ISerializeToJson) -> dict:
        serializer = getMultiAdapter((obj, http_request), iface)
        return serializer()

    return func


@pytest.fixture
def serialize_summary(serialize) -> Callable[[DexterityContent], dict]:
    """Return a helper running a content item through the summary serializer."""

    def func(obj) -> dict:
        return serialize(obj, ISerializeToJsonSummary)

    return func
