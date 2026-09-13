from . import ROLES
from collective.casestudy.content.case_study import CaseStudy
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


#: Workflow bound to the CaseStudy type.
WORKFLOW_ID = "casestudy_workflow"

ACCESS = "Access contents information"
MODIFY = "Modify portal content"
VIEW = "View"

#: Every role checked.
EVERYONE = set(ROLES)

#: Roles that can see a case study before it is listed.
DRAFT_READERS = {
    "Manager",
    "Site Administrator",
    "Reviewer",
    "Editor",
    "Owner",
    "Reader",
    "Contributor",
}

#: Roles that can edit a case study before it is listed.
DRAFT_EDITORS = {"Manager", "Site Administrator", "Reviewer", "Editor", "Owner"}

#: Roles that can edit a listed case study.
LISTED_EDITORS = {"Manager", "Site Administrator", "Editor"}

#: Roles that can edit a verified or archived case study.
LOCKED_EDITORS = {"Manager", "Site Administrator"}

#: Roles holding each permission ``casestudy_workflow`` manages, per state.
PERMISSIONS: dict[str, dict[str, set[str]]] = {
    "created": {ACCESS: DRAFT_READERS, VIEW: DRAFT_READERS, MODIFY: DRAFT_EDITORS},
    "pending": {ACCESS: DRAFT_READERS, VIEW: DRAFT_READERS, MODIFY: DRAFT_EDITORS},
    "listed": {ACCESS: EVERYONE, VIEW: EVERYONE, MODIFY: LISTED_EDITORS},
    "verified": {ACCESS: EVERYONE, VIEW: EVERYONE, MODIFY: LOCKED_EDITORS},
    "archived": {ACCESS: EVERYONE, VIEW: EVERYONE, MODIFY: LOCKED_EDITORS},
}


@pytest.fixture(scope="class")
def portal_type() -> str:
    return "CaseStudy"


@pytest.fixture(scope="class")
def payload(portal_type, case_studies_payload) -> dict:
    return case_studies_payload[0]


class TestCaseStudyFTI:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, portal_type, get_fti) -> None:
        """Bind the site and the FTI of the type under test to the instance."""
        self.portal = portal
        self.fti: DexterityFTI = get_fti(portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Case Study"),
            ("factory", "CaseStudy"),
            ("klass", "collective.casestudy.content.case_study.CaseStudy"),
            ("schema", "collective.casestudy.content.case_study.ICaseStudy"),
            ("add_permission", "cmf.AddPortalContent"),
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
            "collective.casestudy.providers",
            "collective.casestudy.organizations",
            "plone.dublincore",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
            "volto.blocks",
            "volto.navtitle",
            "volto.preview_image_link",
            "volto.head_title",
        )),
    )
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior

    def test_factory(self):
        """The FTI factory returns a CaseStudy."""
        obj = createObject(self.fti.factory)
        assert obj is not None
        assert isinstance(obj, CaseStudy)


class TestCaseStudy:
    def test_workflow_chain(self, portal_type, content_instance):
        """Case studies run a workflow of their own, not the site default."""
        wf_tool = api.portal.get_tool("portal_workflow")
        assert wf_tool.getChainFor(portal_type) == (WORKFLOW_ID,)

    def test_create(self, portal_type, content_instance):
        """Content is created with the expected type and class."""
        assert content_instance.portal_type == portal_type
        assert isinstance(content_instance, CaseStudy)

    def test_indexer_industry(self, content_instance):
        """The industry field is indexed on creation."""
        brains = api.content.find(industry="ngo")
        assert len(brains) == 1
        assert content_instance.UID() == brains[0].UID


class TestCaseStudyWorkflow:
    """Who holds each permission ``casestudy_workflow`` manages, in each state.

    Each test puts the case study in its state with the ``set_state`` fixture,
    so every check runs against the one class-scoped case study, whatever
    state an earlier test left it in. Reaching the states through transitions
    is covered by ``tests/workflow/test_workflow_case_study.py``.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, content_instance, has_permission, set_state) -> None:
        self.case_study = content_instance
        self.has_permission = has_permission
        self.set_state = set_state

    def test_the_expectations_cover_the_workflow(self):
        """Every state and managed permission is checked, and nothing else."""
        wt = api.portal.get_tool("portal_workflow")
        workflow = wt.getWorkflowById(WORKFLOW_ID)
        assert set(PERMISSIONS) == set(workflow.states)
        for state, permissions in PERMISSIONS.items():
            assert set(permissions) == set(workflow.permissions), state

    @pytest.mark.parametrize("state", list(PERMISSIONS))
    def test_set_state_is_the_state_the_workflow_reports(self, state: str):
        """``set_state`` writes the state DCWorkflow reads back."""
        self.set_state(self.case_study, WORKFLOW_ID, state)
        assert api.content.get_state(obj=self.case_study) == state

    def test_set_state_rejects_an_unknown_state(self):
        """A state the workflow does not define is an error, not a fallback."""
        with pytest.raises(ValueError, match="has no state 'published'"):
            self.set_state(self.case_study, WORKFLOW_ID, "published")

    @pytest.mark.parametrize(
        "state,permission,role,expected",
        [
            pytest.param(
                state,
                permission,
                role,
                role in allowed,
                id=f"{state}-{permission}-{role}",
            )
            for state, permissions in PERMISSIONS.items()
            for permission, allowed in permissions.items()
            for role in ROLES
        ],
    )
    def test_permission(self, state: str, permission: str, role: str, expected: bool):
        self.set_state(self.case_study, WORKFLOW_ID, state)
        assert self.has_permission(role, permission, self.case_study) is expected
