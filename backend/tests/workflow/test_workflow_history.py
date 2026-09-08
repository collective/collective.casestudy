"""Workflow history with two workflows on one object.

Each workflow keeps its own entry in ``workflow_history``, keyed by workflow
id, and records its transitions under its **own** state variable -- so a
provider entry says ``workflow_states``, never ``review_state``.

The trap is reading it back. ``getInfoFor(obj, "review_history")`` is
untargeted: it walks the chain and takes the first workflow that offers the
variable, and the publication workflow is always first because the adapter only
ever appends. A provider's transitions are therefore invisible to any caller
that does not pass ``wf_id`` -- which is exactly what core's ``@history``
listing does, and why `collective.multiworkflow` overrides it.
"""

from . import PROVIDER_WORKFLOW
from . import PUBLICATION_WORKFLOW
from plone import api
from plone.dexterity.content import DexterityContent


def entries(obj: DexterityContent, workflow_id: str) -> list:
    """Return the history one workflow recorded on an object.

    :param obj: The object to read.
    :param workflow_id: The workflow whose entries are wanted.
    :returns: That workflow's entries, oldest first.
    """
    return list(obj.workflow_history.get(workflow_id, ()))


class TestEachWorkflowKeepsItsOwnHistory:
    def test_both_workflows_are_present(self, provider: DexterityContent):
        assert set(provider.workflow_history) == {
            PUBLICATION_WORKFLOW,
            PROVIDER_WORKFLOW,
        }

    def test_a_plain_organization_records_only_publication(self, plone_user):
        assert set(plone_user.workflow_history) == {PUBLICATION_WORKFLOW}

    def test_creation_is_recorded_with_no_action(self, provider):
        first = entries(provider, PROVIDER_WORKFLOW)[0]
        assert first["action"] is None
        assert first["workflow_states"] == "created"

    def test_a_provider_entry_uses_its_own_state_variable(self, provider):
        """`review_state` here would mean the two workflows share a variable."""
        first = entries(provider, PROVIDER_WORKFLOW)[0]
        assert "workflow_states" in first
        assert "review_state" not in first

    def test_a_publication_entry_uses_review_state(self, provider):
        first = entries(provider, PUBLICATION_WORKFLOW)[0]
        assert "review_state" in first


class TestTransitionsAreRecordedSeparately:
    def test_a_provider_transition_appends_to_its_own_history(
        self, provider, as_manager
    ):
        before = len(entries(provider, PROVIDER_WORKFLOW))

        as_manager(provider, "verify")

        after = entries(provider, PROVIDER_WORKFLOW)
        assert len(after) == before + 1
        assert after[-1]["action"] == "verify"
        assert after[-1]["workflow_states"] == "verified"

    def test_it_does_not_touch_the_publication_history(self, provider, as_manager):
        before = entries(provider, PUBLICATION_WORKFLOW)

        as_manager(provider, "verify")

        assert entries(provider, PUBLICATION_WORKFLOW) == before

    def test_publishing_does_not_touch_the_provider_history(self, provider):
        before = entries(provider, PROVIDER_WORKFLOW)

        api.content.transition(obj=provider, transition="publish")

        assert entries(provider, PROVIDER_WORKFLOW) == before

    def test_both_histories_grow_independently(self, provider, as_manager):
        api.content.transition(obj=provider, transition="publish")
        as_manager(provider, "list")
        as_manager(provider, "verify")

        assert len(entries(provider, PROVIDER_WORKFLOW)) == 3
        assert len(entries(provider, PUBLICATION_WORKFLOW)) == 2

    def test_the_actor_is_recorded(self, provider, as_manager):
        as_manager(provider, "verify")
        assert entries(provider, PROVIDER_WORKFLOW)[-1]["actor"]


class TestUntargetedReadsMissTheProvider:
    """Why the ``@history`` endpoint had to be overridden."""

    def test_review_history_resolves_to_publication(self, provider, as_manager):
        wt = api.portal.get_tool("portal_workflow")
        as_manager(provider, "verify")

        history = wt.getInfoFor(provider, "review_history")

        actions = [entry.get("action") for entry in history]
        assert "verify" not in actions

    def test_the_provider_history_is_reachable_with_wf_id(self, provider, as_manager):
        wt = api.portal.get_tool("portal_workflow")
        as_manager(provider, "verify")

        history = wt.getInfoFor(provider, "review_history", wf_id=PROVIDER_WORKFLOW)

        assert "verify" in [entry.get("action") for entry in history]
