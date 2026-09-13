"""Fixtures for the two-workflow tests."""

from collections.abc import Callable
from plone import api
from plone.dexterity.content import DexterityContent

import pytest


@pytest.fixture
def provider(portal, providers_payload) -> DexterityContent:
    """An organization whose chain gained ``provider_workflow`` on creation."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **providers_payload[0])


@pytest.fixture
def plone_user(portal, organizations_payload) -> DexterityContent:
    """An organization running the publication workflow alone."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **organizations_payload[0])


@pytest.fixture
def as_manager() -> Callable[..., None]:
    """Return a helper running a provider transition with enough rights."""

    def func(obj: DexterityContent, transition: str) -> None:
        with api.env.adopt_roles(["Manager"]):
            api.content.transition(obj=obj, transition=transition)

    return func
