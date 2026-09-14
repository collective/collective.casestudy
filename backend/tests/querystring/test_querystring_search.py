"""Searching with the listing and verification fields, end to end.

Each criterion runs through the ``querybuilderresults`` view, so a modifier is
judged by what the catalog returns rather than by the dictionary it builds.
"""

from . import ANY
from . import DOCUMENT
from . import EXPECTED
from . import FIELDS
from . import IS_FALSE
from . import IS_TRUE
from . import PLAIN_ORGANIZATION

import pytest


def _param_id(field: str, operation: str) -> str:
    return f"{field}-{'yes' if operation == IS_TRUE else 'no'}"


class TestEachField:
    @pytest.fixture(autouse=True)
    def _setup(self, contents, search) -> None:
        self.search = search

    @pytest.mark.parametrize(
        "field,operation,expected",
        [
            pytest.param(field, operation, ids, id=_param_id(field, operation))
            for (field, operation), ids in EXPECTED.items()
        ],
    )
    def test_matches(self, field: str, operation: str, expected: set[str]):
        assert self.search((field, operation, None)) == expected

    @pytest.mark.parametrize("field", sorted(FIELDS))
    def test_yes_and_no_do_not_overlap(self, field: str):
        yes = self.search((field, IS_TRUE, None))
        no = self.search((field, IS_FALSE, None))
        assert yes & no == set()

    @pytest.mark.parametrize("field", sorted(FIELDS))
    def test_content_outside_the_workflow_matches_neither(self, field: str):
        """A plain organization or a document is neither listed nor unlisted."""
        yes = self.search((field, IS_TRUE, None))
        no = self.search((field, IS_FALSE, None))
        assert {PLAIN_ORGANIZATION, DOCUMENT} & (yes | no) == set()


class TestCombinedCriteria:
    @pytest.fixture(autouse=True)
    def _setup(self, contents, search) -> None:
        self.search = search

    def test_with_a_type_criterion(self):
        """A criterion on another index combines normally."""
        found = self.search(
            ("provider_listed", IS_TRUE, None),
            ("portal_type", ANY, ["Organization"]),
        )
        assert found == {"pv-listed", "pv-verified", "pv-verified-private"}

    def test_with_a_bare_review_state_criterion(self):
        """Published *and* verified, naming the state alone.

        A ``review_state`` value naming no workflow stays on the stock
        ``review_state`` index, so it combines with the field.
        """
        found = self.search(
            ("provider_verified", IS_TRUE, None),
            ("review_state", ANY, ["published"]),
        )
        assert found == {"pv-verified"}

    @pytest.mark.xfail(
        strict=True,
        reason=(
            "a review_state value naming a workflow is also rewritten onto "
            "workflow_states by collective.multiworkflow; the last modifier to "
            "run replaces the other criterion"
        ),
    )
    def test_with_a_qualified_review_state_criterion(self):
        """Published *and* verified, as the collection editor saves the state."""
        found = self.search(
            ("provider_verified", IS_TRUE, None),
            ("review_state", ANY, ["simple_publication_workflow|published"]),
        )
        assert found == {"pv-verified"}

    @pytest.mark.xfail(
        strict=True,
        reason=(
            "both fields are rewritten onto workflow_states; the last modifier "
            "to run replaces the other criterion"
        ),
    )
    def test_listed_but_not_verified(self):
        found = self.search(
            ("case_study_listed", IS_TRUE, None),
            ("case_study_verified", IS_FALSE, None),
        )
        assert found == {"cs-listed"}
