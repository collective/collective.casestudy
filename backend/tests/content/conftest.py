from . import ANONYMOUS
from . import OWNER
from . import PASSWORD
from . import ROLES
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from collections.abc import Callable
from collections.abc import Generator
from DateTime import DateTime
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


@pytest.fixture(scope="class")
def users(portal) -> dict[str, str]:
    """Create a user for every role a permission check runs as.

    Every user is a Member; each role but ``Member`` and ``Owner`` is granted
    on top of that, globally. ``Owner`` is a local role, so
    :func:`has_permission` grants it on the object being checked.
    ``Anonymous`` needs no user.

    Real users rather than :func:`plone.api.env.adopt_roles`: adopted roles
    are proxy roles, which replace a user's roles outright and bypass the
    shortcut granting everyone a permission mapped to ``Anonymous``. A Manager
    would read as unable to view a public item.

    :param portal: Plone site.
    :returns: Mapping of role to username.
    """
    usernames: dict[str, str] = {}
    with api.env.adopt_roles(["Manager"]):
        for role in ROLES:
            if role == ANONYMOUS:
                continue
            username = role.lower().replace(" ", "-")
            roles = ["Member"] if role in ("Member", OWNER) else ["Member", role]
            api.user.create(
                email=f"{username}@plone.org",
                username=username,
                password=PASSWORD,
                roles=roles,
            )
            usernames[role] = username
    return usernames


@pytest.fixture
def has_permission(users) -> Callable[[str, str, DexterityContent], bool]:
    """Return a helper checking a permission as a user holding one role.

    :param users: Mapping of role to username, from :func:`users`.
    :returns: Callable taking a role, a permission title and an object, and
        returning whether a user with that role holds the permission on it.
    """

    def func(role: str, permission: str, obj: DexterityContent) -> bool:
        if role == ANONYMOUS:
            current = getSecurityManager()
            noSecurityManager()
            try:
                return bool(getSecurityManager().checkPermission(permission, obj))
            finally:
                setSecurityManager(current)
        username = users[role]
        if role == OWNER:
            with api.env.adopt_roles(["Manager"]):
                api.user.grant_roles(username=username, obj=obj, roles=[OWNER])
        return api.user.has_permission(permission, username=username, obj=obj)

    return func


@pytest.fixture(scope="session")
def set_state() -> Callable[[DexterityContent, str, str], None]:
    """Return a helper putting an object in a state of one of its workflows.

    The helper records a status entry and then applies the state's role
    mappings -- what DCWorkflow does at the end of a transition -- so a
    permission check can run against any state, whatever state the object is
    in beforehand.

    Not :func:`plone.api.content.transition` with ``to_state``: it can only
    reach a state some transition leads to, and nothing leads back to a
    workflow's initial state, so an object shared by a test class could not
    return to it once an earlier test moved it on.

    The state is written under the workflow's own state variable:
    ``review_state`` for ``casestudy_workflow``, ``workflow_states`` for an
    additional workflow such as ``provider_workflow``. DCWorkflow reads any
    other key as "no status" and falls back to the initial state silently.

    :returns: Callable taking an object, a workflow id and a state id.
    :raises ValueError: When the workflow has no such state.
    """

    def func(obj: DexterityContent, workflow_id: str, state: str) -> None:
        wt = api.portal.get_tool("portal_workflow")
        workflow = wt.getWorkflowById(workflow_id)
        if state not in workflow.states:
            raise ValueError(f"{workflow_id} has no state {state!r}")
        wt.setStatusOf(
            workflow_id,
            obj,
            {
                "action": None,
                "actor": "admin",
                "comments": "",
                workflow.state_var: state,
                "time": DateTime(),
            },
        )
        workflow.updateRoleMappingsFor(obj)

    return func
