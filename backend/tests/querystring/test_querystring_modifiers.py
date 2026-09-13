"""The ``IParsedQueryIndexModifier`` utilities behind the listing fields.

The utilities are looked up by name, the way ``plone.app.querystring`` finds
them, rather than imported: what matters is what is registered under each
field's name, not which class implements it.

These tests hold the criterion to the ``workflow_states`` index contract.
Values there are always qualified -- ``<workflow-id>|<state-id>`` -- so a bare
state id matches nothing, and a case study field that does not name
``casestudy_workflow`` cannot tell a verified case study from a verified
provider.
"""

from . import FIELDS
from . import LISTED_STATES
from . import VERIFIED_STATES
from collective.multiworkflow.indexers import parse_state
from collective.multiworkflow.indexers import WORKFLOW_STATES
from plone import api
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from zope.component import getUtility
from zope.component import queryUtility

import pytest


def criterion_values(query: dict) -> list[str]:
    """Return the state values a parsed criterion names.

    :param query: The criterion a modifier returned.
    :returns: The values under ``query``, or under ``not`` for an exclusion.
    """
    values = query.get("query") or query.get("not") or []
    return [values] if isinstance(values, str) else list(values)


class TestRegistered:
    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        self.portal = portal

    @pytest.mark.parametrize("field", sorted(FIELDS))
    def test_a_modifier_is_registered_for_the_field(self, field: str):
        assert queryUtility(IParsedQueryIndexModifier, name=field) is not None

    @pytest.mark.parametrize("field", sorted(FIELDS))
    def test_the_field_is_offered_to_editors(self, field: str):
        """A modifier without a registry record is a criterion nobody can pick."""
        record = f"plone.app.querystring.field.{field}.title"
        assert api.portal.get_registry_record(record)


class TestRewrite:
    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        self.portal = portal

    @staticmethod
    def rewrite(field: str, flag: bool) -> tuple[str, dict]:
        """Run a field's modifier on the criterion a Yes or No operation parses to.

        :param field: Querystring field name.
        :param flag: ``True`` for Yes, ``False`` for No.
        :returns: The index name and criterion the modifier returns.
        """
        modifier = getUtility(IParsedQueryIndexModifier, name=field)
        return modifier({"query": flag})

    @pytest.mark.parametrize("flag", [True, False])
    @pytest.mark.parametrize("field", sorted(FIELDS))
    def test_it_targets_the_workflow_states_index(self, field: str, flag: bool):
        index, _ = self.rewrite(field, flag)
        assert index == WORKFLOW_STATES

    @pytest.mark.parametrize("flag", [True, False])
    @pytest.mark.parametrize("field", sorted(FIELDS))
    def test_no_criterion_is_empty(self, field: str, flag: bool):
        """An empty criterion matches no content at all, whatever the flag."""
        _, query = self.rewrite(field, flag)
        assert criterion_values(query) != []

    @pytest.mark.parametrize("flag", [True, False])
    @pytest.mark.parametrize("field", sorted(FIELDS))
    def test_values_are_qualified_with_the_field_workflow(self, field: str, flag: bool):
        """A bare state id matches nothing in ``workflow_states``."""
        _, query = self.rewrite(field, flag)
        for value in criterion_values(query):
            workflow_id, _ = parse_state(value)
            assert workflow_id == FIELDS[field], value

    @pytest.mark.parametrize(
        "field,states",
        [
            ("case_study_verified", VERIFIED_STATES),
            ("case_study_listed", LISTED_STATES),
            ("provider_verified", VERIFIED_STATES),
            ("provider_listed", LISTED_STATES),
        ],
    )
    def test_yes_names_the_matching_states(self, field: str, states: set[str]):
        _, query = self.rewrite(field, True)
        named = {parse_state(value)[1] for value in query["query"]}
        assert named == states
