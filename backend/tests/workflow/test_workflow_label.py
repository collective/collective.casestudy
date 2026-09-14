"""The label ``provider_workflow`` is shown under.

``<plone:additionalworkflows />`` takes a ``label`` naming a contributed
workflow wherever the user interface names it -- the ``title`` of its
``@workflow`` chain entry, the Volto workflow control and history, and the
options of the *Review state* collection criterion -- in place of the
workflow's own title.
"""

from collective.casestudy.subscribers.organization import WORKFLOW_ID
from collective.multiworkflow.declaration import workflow_label
from collective.multiworkflow.utils.workflow import format_state
from plone import api
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from zope.component import getUtility
from zope.i18nmessageid import Message
from zope.schema.interfaces import IVocabularyFactory

import pytest


#: The label the directive declares for ``provider_workflow``.
LABEL = "Provider listing"

#: The vocabulary behind the *Review state* collection criterion.
WORKFLOW_STATES_VOCABULARY = "collective.multiworkflow.vocabularies.WorkflowStates"


class TestProviderWorkflowLabel:
    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        wt = api.portal.get_tool("portal_workflow")
        self.workflow: DCWorkflowDefinition = wt.getWorkflowById(WORKFLOW_ID)

    def test_label_names_the_workflow(self):
        assert workflow_label(self.workflow) == LABEL

    def test_label_is_a_message_of_the_package_domain(self):
        """The ZCML file declaring the label sets the domain it translates in."""
        label = workflow_label(self.workflow)
        assert isinstance(label, Message)
        assert label.domain == "collective.casestudy"

    def test_title_is_left_alone(self):
        """Only what the user interface shows changes, not the definition."""
        assert self.workflow.title == "Provider"

    def test_review_state_options_use_the_label(self, portal):
        factory = getUtility(IVocabularyFactory, WORKFLOW_STATES_VOCABULARY)
        term = factory(portal).getTerm(format_state(WORKFLOW_ID, "verified"))
        assert term.title == f"{LABEL}: Verified"
