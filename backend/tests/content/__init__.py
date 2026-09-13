"""Tests for the content types.

Shared values live here so the modules and ``conftest`` import them relatively.
"""

ANONYMOUS = "Anonymous"
OWNER = "Owner"

#: Roles a workflow permission test checks, from least to most privileged.
ROLES: tuple[str, ...] = (
    ANONYMOUS,
    "Member",
    "Reader",
    "Contributor",
    "Editor",
    "Reviewer",
    OWNER,
    "Site Administrator",
    "Manager",
)

#: Password of the users created by the ``users`` fixture.
PASSWORD = "workflow-permissions-2026"  # noQA: S105
