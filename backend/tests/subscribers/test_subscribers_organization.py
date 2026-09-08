"""The Organization subscribers.

``provider_workflow`` reaches an organization through the ``IProvider``
marker, and nothing sets that marker declaratively -- these handlers are what
turn the ``is_provider`` field into a workflow chain entry and back again.
"""

from collective.casestudy.behaviors.provider_info import IProvider
from collective.casestudy.subscribers.organization import check_provider_status
from collective.casestudy.subscribers.organization import update_role_mappings
from collective.casestudy.subscribers.organization import WORKFLOW_ID
from collective.multiworkflow import api as mw_api
from plone import api
from plone.dexterity.content import DexterityContent
from zope.lifecycleevent import modified

import pytest


VIEW_PERMISSION = "collective.casestudy: View Provider Information"


def granted_roles(obj: DexterityContent, permission: str) -> set[str]:
    """Return the roles a permission is granted to on an object.

    :param obj: The object whose permission map is read.
    :param permission: Title of the permission.
    :returns: The role names currently selected for that permission.
    """
    return {
        role["name"] for role in obj.rolesOfPermission(permission) if role["selected"]
    }


@pytest.fixture
def provider(portal, providers_payload) -> DexterityContent:
    """An organization created with ``is_provider`` already true."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **providers_payload[0])


@pytest.fixture
def plone_user(portal, organizations_payload) -> DexterityContent:
    """An organization that never opted in to being a provider."""
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **organizations_payload[0])


class TestMarkerFollowsTheField:
    """``is_provider`` is what decides whether the marker is applied."""

    def test_provider_is_marked_on_creation(self, provider):
        assert IProvider.providedBy(provider)

    def test_plain_organization_is_not_marked(self, plone_user):
        assert not IProvider.providedBy(plone_user)

    def test_opting_in_applies_the_marker(self, plone_user):
        plone_user.is_provider = True
        modified(plone_user)
        assert IProvider.providedBy(plone_user)

    def test_opting_out_removes_the_marker(self, provider):
        provider.is_provider = False
        modified(provider)
        assert not IProvider.providedBy(provider)

    def test_opting_in_and_out_again_leaves_no_marker(self, plone_user):
        """The two branches have to be each other's inverse.

        A handler that only ever adds would pass every test above.
        """
        plone_user.is_provider = True
        modified(plone_user)
        plone_user.is_provider = False
        modified(plone_user)
        assert not IProvider.providedBy(plone_user)

    def test_a_repeated_save_keeps_the_marker(self, provider):
        """Saving without touching the field must not toggle anything."""
        modified(provider)
        assert IProvider.providedBy(provider)


class TestWorkflowChain:
    """The marker is only useful because it changes the chain."""

    def test_provider_gains_the_workflow(self, provider, portal):
        wt = api.portal.get_tool("portal_workflow")
        assert WORKFLOW_ID in wt.getChainFor(provider)

    def test_plain_organization_does_not(self, plone_user, portal):
        wt = api.portal.get_tool("portal_workflow")
        assert WORKFLOW_ID not in wt.getChainFor(plone_user)

    def test_the_type_chain_is_kept(self, provider, portal):
        """The additional workflow appends; it never replaces."""
        wt = api.portal.get_tool("portal_workflow")
        chain = wt.getChainFor(provider)
        assert len(chain) > 1
        assert chain[-1] == WORKFLOW_ID

    def test_opting_out_drops_the_workflow(self, provider, portal):
        provider.is_provider = False
        modified(provider)
        wt = api.portal.get_tool("portal_workflow")
        assert WORKFLOW_ID not in wt.getChainFor(provider)


class TestRoleMappings:
    """What the handler exists to keep correct."""

    def test_provider_starts_in_the_initial_state(self, provider):
        assert mw_api.get_states(provider).get(WORKFLOW_ID) == "created"

    def test_initial_state_is_not_publicly_viewable(self, provider):
        """``created`` is a draft: the provider fields are staff-only."""
        assert "Anonymous" not in granted_roles(provider, VIEW_PERMISSION)

    def test_mappings_follow_a_transition(self, provider):
        api.content.transition(obj=provider, transition="verify")
        assert "Anonymous" in granted_roles(provider, VIEW_PERMISSION)

    def test_mappings_are_rewritten_for_the_current_state(self, provider):
        """The handler applies the state the object is in, not a fixed one.

        This is the regression that matters: role mappings written while the
        object had no status for the workflow describe the initial state, and
        only a later pass over the *current* state corrects them.
        """
        api.content.transition(obj=provider, transition="verify")
        assert mw_api.get_states(provider).get(WORKFLOW_ID) == "verified"
        update_role_mappings(provider)
        assert "Anonymous" in granted_roles(provider, VIEW_PERMISSION)

    def test_a_plain_organization_gets_no_provider_mappings(self, plone_user):
        """Nothing should have written the workflow's permission map."""
        assert granted_roles(plone_user, VIEW_PERMISSION) != {"Anonymous", "Member"}


class TestCheckProviderStatus:
    """The function both handlers delegate to."""

    def test_it_is_idempotent(self, provider):
        before = granted_roles(provider, VIEW_PERMISSION)
        check_provider_status(provider)
        check_provider_status(provider)
        assert granted_roles(provider, VIEW_PERMISSION) == before
        assert IProvider.providedBy(provider)

    def test_it_does_nothing_for_a_plain_organization(self, plone_user):
        before = granted_roles(plone_user, VIEW_PERMISSION)
        check_provider_status(plone_user)
        assert granted_roles(plone_user, VIEW_PERMISSION) == before
        assert not IProvider.providedBy(plone_user)
