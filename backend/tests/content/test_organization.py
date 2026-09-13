from . import ROLES
from collective.casestudy.content.organization import Organization
from collective.casestudy.vocabularies.organization import DEFAULT_FACET
from collective.multiworkflow import api as mw_api
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


#: Workflow an organization gains once it is flagged as a provider.
PROVIDER_WORKFLOW = "provider_workflow"

#: The chain a provider runs: the site default, then the provider workflow.
PROVIDER_CHAIN = ("simple_publication_workflow", PROVIDER_WORKFLOW)

EDIT_PROVIDER = "collective.casestudy: Edit Provider Information"
MANAGE_LISTING = "collective.casestudy: Manage Provider Listing"
VIEW_PROVIDER = "collective.casestudy: View Provider Information"

#: Every role checked. A state mapping a permission to ``Anonymous`` grants it
#: to every user, whatever their roles.
EVERYONE = set(ROLES)

#: Roles that manage the listing of a provider that is not archived.
LISTING_MANAGERS = {"Manager", "Site Administrator", "Reviewer", "Editor"}

#: Roles that can see and edit provider information before it is listed.
DRAFT_EDITORS = LISTING_MANAGERS | {"Owner"}

#: Roles that can edit the information of a listed provider.
LISTED_EDITORS = {"Manager", "Site Administrator", "Editor"}

#: Roles left in charge of a verified or archived provider.
LOCKED_EDITORS = {"Manager", "Site Administrator"}

#: Roles holding each permission ``provider_workflow`` manages, per state.
PERMISSIONS: dict[str, dict[str, set[str]]] = {
    "created": {
        VIEW_PROVIDER: DRAFT_EDITORS,
        EDIT_PROVIDER: DRAFT_EDITORS,
        MANAGE_LISTING: LISTING_MANAGERS,
    },
    "pending": {
        VIEW_PROVIDER: DRAFT_EDITORS,
        EDIT_PROVIDER: DRAFT_EDITORS,
        MANAGE_LISTING: LISTING_MANAGERS,
    },
    "listed": {
        VIEW_PROVIDER: EVERYONE,
        EDIT_PROVIDER: LISTED_EDITORS,
        MANAGE_LISTING: LISTING_MANAGERS,
    },
    "verified": {
        VIEW_PROVIDER: EVERYONE,
        EDIT_PROVIDER: LOCKED_EDITORS,
        MANAGE_LISTING: LISTING_MANAGERS,
    },
    "archived": {
        VIEW_PROVIDER: EVERYONE,
        EDIT_PROVIDER: LOCKED_EDITORS,
        MANAGE_LISTING: LOCKED_EDITORS,
    },
}


@pytest.fixture(scope="class")
def portal_type() -> str:
    return "Organization"


@pytest.fixture(scope="class")
def payload(portal_type, organizations_payload) -> dict:
    return organizations_payload[0]


class TestOrganizationFTI:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, portal_type, get_fti) -> None:
        """Bind the site and the FTI of the type under test to the instance."""
        self.portal = portal
        self.fti: DexterityFTI = get_fti(portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Organization"),
            ("factory", "Organization"),
            ("klass", "collective.casestudy.content.organization.Organization"),
            ("schema", "collective.casestudy.content.organization.IOrganization"),
            ("add_permission", "collective.casestudy.organization.add"),
            ("global_allow", True),
        ],
    )
    def test_fti(self, attr: str, expected):
        """Test FTI values."""
        fti = self.fti

        assert isinstance(fti, DexterityFTI)
        assert getattr(fti, attr) == expected

    @pytest.mark.parametrize(
        "idx,behavior",
        enumerate((
            "plone.basic",
            "volto.preview_image_link",
            "collective.casestudy.contact_info",
            "plonegovbr.socialmedia.links",
            "collective.casestudy.address_info",
            "collective.casestudy.provider_info",
            "plone.categorization",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
        )),
    )
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior

    def test_factory(self):
        """The FTI factory returns an Organization."""
        obj = createObject(self.fti.factory)
        assert obj is not None
        assert isinstance(obj, Organization)

    def test_addable_at_portal_root(self, portal_type):
        """Organization replaces Provider as the globally addable type."""
        addable = [fti.getId() for fti in self.portal.allowedContentTypes()]
        assert portal_type in addable

    def test_workflow_chain(self, portal_type):
        """Organization uses the site default workflow.

        Contact information is protected by the acquired rolemap grants
        rather than by per-state permission maps, so no workflow of its own
        is needed.
        """
        wf_tool = api.portal.get_tool("portal_workflow")
        assert wf_tool.getChainFor(portal_type) == ("simple_publication_workflow",)


class TestOrganization:
    def test_create(self, portal_type, content_instance):
        """Content is created with the expected type and class."""
        assert content_instance.portal_type == portal_type
        assert isinstance(content_instance, Organization)

    def test_indexer_facets(self, content_instance):
        """A plain organization gets the default facet, not the provider one."""
        brain = api.content.find(UID=content_instance.UID())[0]
        assert brain.facets == [DEFAULT_FACET]


class TestProviderWorkflow:
    """Who holds each permission ``provider_workflow`` manages, in each state.

    The organization is created from a provider payload, so its chain gains
    ``provider_workflow`` after the publication workflow. Each test puts it in
    its state with the ``set_state`` fixture, so every check runs against the
    one class-scoped provider, whatever state an earlier test left it in.
    Reaching the states through transitions, and the two workflows leaving
    each other's permissions alone, is covered by ``tests/workflow/``.
    """

    @pytest.fixture(scope="class")
    def payload(self, providers_payload) -> dict:
        """Create the organization flagged as a provider."""
        return providers_payload[0]

    @pytest.fixture(autouse=True)
    def _setup(self, content_instance, has_permission, set_state) -> None:
        self.provider = content_instance
        self.has_permission = has_permission
        self.set_state = set_state

    def test_a_provider_runs_the_provider_workflow(self):
        """The checks below only mean something for an actual provider.

        ``set_state`` applies a workflow's role mappings whether or not the
        workflow is in the object's chain.
        """
        wt = api.portal.get_tool("portal_workflow")
        assert wt.getChainFor(self.provider) == PROVIDER_CHAIN

    def test_the_expectations_cover_the_workflow(self):
        """Every state and managed permission is checked, and nothing else."""
        wt = api.portal.get_tool("portal_workflow")
        workflow = wt.getWorkflowById(PROVIDER_WORKFLOW)
        assert set(PERMISSIONS) == set(workflow.states)
        for state, permissions in PERMISSIONS.items():
            assert set(permissions) == set(workflow.permissions), state

    @pytest.mark.parametrize("state", list(PERMISSIONS))
    def test_set_state_is_the_state_the_workflow_reports(self, state: str):
        """``set_state`` writes under ``provider_workflow``'s state variable."""
        self.set_state(self.provider, PROVIDER_WORKFLOW, state)
        assert mw_api.get_state(self.provider, workflow_id=PROVIDER_WORKFLOW) == state

    @pytest.mark.parametrize(
        "state,permission,role,expected",
        [
            pytest.param(
                state,
                permission,
                role,
                role in allowed,
                id=f"{state}-{permission.split(': ')[-1]}-{role}",
            )
            for state, permissions in PERMISSIONS.items()
            for permission, allowed in permissions.items()
            for role in ROLES
        ],
    )
    def test_permission(self, state: str, permission: str, role: str, expected: bool):
        self.set_state(self.provider, PROVIDER_WORKFLOW, state)
        assert self.has_permission(role, permission, self.provider) is expected
