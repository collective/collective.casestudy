"""Tests for the provider workflow as the *second* workflow in a chain.

An organization flagged as a provider runs two workflows at once, and almost
everything that can go wrong here goes wrong quietly: a permission claimed by
both is simply overwritten by whichever transitioned last, a transition id
present in both resolves to the first workflow in the chain, and an untargeted
``review_history`` read never reaches past the publication workflow.

A case study runs ``casestudy_workflow`` alone, bound to its type. It shares
the provider workflow's states but manages the standard content permissions.

Shared values live here so the modules and ``conftest`` import them relatively,
following the layout `collective.multiworkflow`'s own suite uses.
"""

from AccessControl.Permission import Permission
from typing import Any


PUBLICATION_WORKFLOW = "simple_publication_workflow"
PROVIDER_WORKFLOW = "provider_workflow"

#: The chain an organization that has not opted in runs.
BASE_CHAIN = (PUBLICATION_WORKFLOW,)

#: The chain a provider runs. The additional workflow is always appended.
PROVIDER_CHAIN = (PUBLICATION_WORKFLOW, PROVIDER_WORKFLOW)

VIEW_PROVIDER = "collective.casestudy: View Provider Information"
EDIT_PROVIDER = "collective.casestudy: Edit Provider Information"
MANAGE_LISTING = "collective.casestudy: Manage Provider Listing"

#: Everything ``provider_workflow`` is expected to manage, and nothing else.
PROVIDER_PERMISSIONS = {VIEW_PROVIDER, EDIT_PROVIDER, MANAGE_LISTING}

#: One of the three the publication workflow manages. Nothing in this package
#: may claim it, or the two workflows fight over the mapping.
PUBLICATION_PERMISSION = "Modify portal content"

CASESTUDY_WORKFLOW = "casestudy_workflow"

ACCESS = "Access contents information"
MODIFY = "Modify portal content"
VIEW = "View"

#: Everything ``casestudy_workflow`` is expected to manage, and nothing else.
CASESTUDY_PERMISSIONS = {ACCESS, MODIFY, VIEW}


def roles_for(obj: Any, permission: str) -> tuple[str, ...]:
    """Read the roles a permission is mapped to on one object.

    Reads the mangled attribute ``modifyRolesForPermission`` writes -- which is
    what a workflow's role mapping actually sets -- rather than going through
    ``rolesOfPermission``, which needs the permission declared in the class's
    ``__ac_permissions__``.

    :param obj: Object to read the mapping from.
    :param permission: Title of the permission, as workflows name it.
    :returns: The roles holding the permission, sorted; empty when the object
        acquires the mapping instead of defining it.
    """
    roles = Permission(permission, (), obj).getRoles(default=())
    return tuple(sorted(roles))
