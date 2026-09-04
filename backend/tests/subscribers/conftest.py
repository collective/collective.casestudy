from collections.abc import Callable
from copy import deepcopy
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFCore.indexing import processQueue
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import pytest


@pytest.fixture
def facets_of(portal) -> Callable[[DexterityContent], list[str]]:
    """Return a helper reading an object's indexed facets.

    CMFCore queues index operations and applies them at the transaction
    boundary, so without ``processQueue`` a test reads the value from before
    the subscriber ran.
    """

    def func(obj: DexterityContent) -> list[str]:
        processQueue()
        return list(api.content.find(UID=obj.UID())[0].facets)

    return func


@pytest.fixture
def organization(portal, organizations_payload) -> DexterityContent:
    """An organization no case study points at yet."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **organizations_payload[0])


@pytest.fixture
def other_organization(portal, organizations_payload) -> DexterityContent:
    """A second organization, so cross-talk is observable."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **organizations_payload[1])


@pytest.fixture
def make_case_study(portal, case_studies_payload) -> Callable[..., DexterityContent]:
    """Return a factory creating a case study, optionally with relations.

    Relations are passed to ``api.content.create`` rather than added
    afterwards, so the object is created the way a REST API POST or an add
    form creates it -- with the relations already in place when
    ``IObjectAddedEvent`` fires.
    """

    def func(index: int = 0, organizations: list | None = None, **extra):
        payload = deepcopy(case_studies_payload[index])
        payload.update(extra)
        if organizations is not None:
            intids = getUtility(IIntIds)
            payload["organizations"] = [
                RelationValue(intids.getId(item)) for item in organizations
            ]
        with api.env.adopt_roles(["Manager"]):
            return api.content.create(container=portal, **payload)

    return func
