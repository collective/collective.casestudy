"""Permissions across the chain.

Two workflows on one object compose only while the permission sets they manage
are **disjoint**. An overlap is not an error anywhere in Plone: both workflows
write the mapping, and the one that transitioned last silently wins. So the
disjointness is asserted directly, not assumed.
"""

from . import EDIT_PROVIDER
from . import MANAGE_LISTING
from . import PROVIDER_PERMISSIONS
from . import PROVIDER_WORKFLOW
from . import PUBLICATION_PERMISSION
from . import PUBLICATION_WORKFLOW
from . import roles_for
from . import VIEW_PROVIDER
from collective.multiworkflow import api as mw_api
from plone import api
from plone.dexterity.content import DexterityContent

import pytest


class TestSetsAreDisjoint:
    """The guarantee everything else in this module rests on."""

    def test_no_permission_is_claimed_twice(self, provider: DexterityContent):
        """`collective.multiworkflow` reports an overlap; there must be none."""
        assert mw_api.conflicting_permissions(provider) == {}

    def test_a_plain_organization_cannot_conflict(self, plone_user):
        """A single-workflow chain has nothing to conflict with."""
        assert mw_api.conflicting_permissions(plone_user) == {}

    def test_provider_workflow_manages_only_its_own(self, provider):
        wt = api.portal.get_tool("portal_workflow")
        workflow = wt.getWorkflowById(PROVIDER_WORKFLOW)
        assert set(workflow.permissions) == PROVIDER_PERMISSIONS

    def test_it_claims_no_publication_permission(self, provider):
        """Claiming `View` here would break publication, silently."""
        wt = api.portal.get_tool("portal_workflow")
        publication = set(wt.getWorkflowById(PUBLICATION_WORKFLOW).permissions)
        provider_wf = set(wt.getWorkflowById(PROVIDER_WORKFLOW).permissions)
        assert publication & provider_wf == set()


class TestNeitherWorkflowDisturbsTheOther:
    """Disjoint sets compose -- asserted by moving each and watching both."""

    def test_publication_leaves_provider_permissions_alone(self, provider, as_manager):
        as_manager(provider, "verify")
        before = {p: roles_for(provider, p) for p in PROVIDER_PERMISSIONS}

        api.content.transition(obj=provider, transition="publish")

        after = {p: roles_for(provider, p) for p in PROVIDER_PERMISSIONS}
        assert after == before

    def test_provider_leaves_publication_permissions_alone(self, provider, as_manager):
        api.content.transition(obj=provider, transition="publish")
        before = roles_for(provider, PUBLICATION_PERMISSION)

        as_manager(provider, "verify")

        assert roles_for(provider, PUBLICATION_PERMISSION) == before

    def test_a_published_draft_provider_keeps_both_mappings(self, provider):
        """The combination the site actually ships: public page, draft listing."""
        api.content.transition(obj=provider, transition="publish")

        assert "Anonymous" not in roles_for(provider, VIEW_PROVIDER)
        assert roles_for(provider, PUBLICATION_PERMISSION) != ()


class TestMappingsPerState:
    """Every managed permission, in every state -- not just `View`."""

    @pytest.mark.parametrize(
        "transitions,expected",
        [
            ([], False),
            (["list"], True),
            (["verify"], True),
            (["list", "verify"], True),
            (["archive"], True),
            (["list", "review"], False),
        ],
    )
    def test_public_readability_follows_the_state(
        self, provider, as_manager, transitions: list[str], expected: bool
    ):
        for transition in transitions:
            as_manager(provider, transition)
        assert ("Anonymous" in roles_for(provider, VIEW_PROVIDER)) is expected

    def test_editing_narrows_once_verified(self, provider, as_manager):
        """An organization stops editing its own provider fields when verified.

        `created` grants Edit to the Owner; `verified` does not. Approving a
        listing freezes what was approved.
        """
        assert "Owner" in roles_for(provider, EDIT_PROVIDER)

        as_manager(provider, "verify")

        assert "Owner" not in roles_for(provider, EDIT_PROVIDER)
        assert roles_for(provider, EDIT_PROVIDER) == ("Manager", "Site Administrator")

    def test_editing_narrows_further_than_listing(self, provider, as_manager):
        """`listed` drops the Owner but keeps the Editor; `verified` drops both."""
        as_manager(provider, "list")
        listed = roles_for(provider, EDIT_PROVIDER)
        assert "Editor" in listed
        assert "Owner" not in listed

        as_manager(provider, "verify")

        assert "Editor" not in roles_for(provider, EDIT_PROVIDER)

    def test_managing_the_listing_never_reaches_the_owner(self, provider, as_manager):
        """Claiming provider status is the site's call, in every state."""
        for transition in [None, "list", "verify", "archive"]:
            if transition:
                as_manager(provider, transition)
            assert "Owner" not in roles_for(provider, MANAGE_LISTING)

    def test_archiving_locks_editing_down(self, provider, as_manager):
        as_manager(provider, "archive")
        assert roles_for(provider, EDIT_PROVIDER) == ("Manager", "Site Administrator")


class TestPlainOrganizationIsUntouched:
    """Content that never opted in must not gain the workflow's mappings."""

    def test_it_runs_one_workflow(self, plone_user):
        wt = api.portal.get_tool("portal_workflow")
        assert PROVIDER_WORKFLOW not in wt.getChainFor(plone_user)

    @pytest.mark.parametrize("permission", sorted(PROVIDER_PERMISSIONS))
    def test_no_provider_mapping_is_written(self, plone_user, permission: str):
        """An empty tuple means the object acquires, rather than defining."""
        assert roles_for(plone_user, permission) == ()
