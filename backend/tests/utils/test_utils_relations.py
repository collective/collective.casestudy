"""Reading relations from both ends.

Every relation walk in the package goes through here, so the guard against a
deleted object is asserted once, on the primitives, rather than four times on
their callers.
"""

from collective.casestudy.utils.relations import case_studies_for_organization
from collective.casestudy.utils.relations import related_from_field
from collective.casestudy.utils.relations import RELATIONSHIPS
from collective.casestudy.utils.relations import sources_of
from collective.casestudy.utils.relations import targets_of
from copy import deepcopy
from plone import api
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import pytest


@pytest.fixture
def organization(portal, organizations_payload):
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **organizations_payload[0])


@pytest.fixture
def provider(portal, providers_payload):
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(container=portal, **providers_payload[0])


@pytest.fixture
def make_case_study(portal, case_studies_payload):
    def func(index=0, **relations):
        payload = deepcopy(case_studies_payload[index])
        intids = getUtility(IIntIds)
        for name, targets in relations.items():
            payload[name] = [RelationValue(intids.getId(t)) for t in targets]
        with api.env.adopt_roles(["Manager"]):
            return api.content.create(container=portal, **payload)

    return func


@pytest.fixture
def delete():
    def func(obj):
        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=obj, check_linkintegrity=False)

    return func


class TestTargetsOf:
    """Forwards: a relation field resolved to what it points at."""

    def test_empty(self):
        assert targets_of([]) == []

    def test_resolves(self, make_case_study, organization):
        case_study = make_case_study(organizations=[organization])
        assert targets_of(case_study.organizations) == [organization]

    def test_keeps_order(self, make_case_study, organization, provider):
        case_study = make_case_study(organizations=[organization, provider])
        assert targets_of(case_study.organizations) == [organization, provider]

    def test_skips_a_deleted_target(self, make_case_study, organization, delete):
        case_study = make_case_study(organizations=[organization])
        delete(organization)
        assert targets_of(case_study.organizations) == []

    def test_keeps_the_survivors(self, make_case_study, organization, provider, delete):
        """One broken relation must not cost the rest of the list."""
        case_study = make_case_study(organizations=[organization, provider])
        delete(organization)
        assert targets_of(case_study.organizations) == [provider]


class TestSourcesOf:
    """Backwards: relation-catalog entries resolved to what points at them."""

    def test_empty(self):
        assert sources_of([]) == []

    def test_resolves(self, make_case_study, organization):
        case_study = make_case_study(organizations=[organization])
        relations = api.relation.get(target=organization, relationship="organizations")
        assert sources_of(relations) == [case_study]

    def test_skips_a_deleted_source(self, make_case_study, organization, delete):
        case_study = make_case_study(organizations=[organization])
        relations = list(
            api.relation.get(target=organization, relationship="organizations")
        )
        delete(case_study)
        assert sources_of(relations) == []


class TestRelatedFromField:
    """The field lookup the indexer and the subscriber share."""

    def test_resolves(self, make_case_study, organization):
        case_study = make_case_study(organizations=[organization])
        assert related_from_field(case_study, "organizations") == [organization]

    def test_reads_the_named_field_only(self, make_case_study, organization, provider):
        case_study = make_case_study(organizations=[organization], providers=[provider])
        assert related_from_field(case_study, "organizations") == [organization]
        assert related_from_field(case_study, "providers") == [provider]

    def test_unset_field(self, make_case_study):
        assert related_from_field(make_case_study(), "organizations") == []

    def test_missing_field(self):
        """The field comes from a behavior a site may have switched off."""

        class WithoutTheBehavior:
            pass

        assert related_from_field(WithoutTheBehavior(), "organizations") == []

    def test_field_set_to_none(self, make_case_study):
        """An unset relation list reads as None, not as an empty one."""
        case_study = make_case_study()
        case_study.organizations = None
        assert related_from_field(case_study, "organizations") == []

    def test_skips_a_deleted_target(self, make_case_study, organization, delete):
        case_study = make_case_study(organizations=[organization])
        delete(organization)
        assert related_from_field(case_study, "organizations") == []


class TestCaseStudiesForOrganization:
    """The two buckets, read from the organization's side."""

    def test_both_keys_always_present(self, organization):
        assert set(case_studies_for_organization(organization)) == set(
            RELATIONSHIPS.values()
        )

    def test_empty_when_nothing_points_at_it(self, organization):
        assert case_studies_for_organization(organization) == {
            "provided": [],
            "received": [],
        }

    def test_received(self, make_case_study, organization):
        case_study = make_case_study(organizations=[organization])
        assert case_studies_for_organization(organization)["received"] == [case_study]

    def test_provided(self, make_case_study, provider):
        case_study = make_case_study(providers=[provider])
        assert case_studies_for_organization(provider)["provided"] == [case_study]

    def test_the_buckets_stay_apart(self, make_case_study, organization):
        make_case_study(organizations=[organization])
        assert case_studies_for_organization(organization)["provided"] == []

    def test_a_neighbour_is_not_reported(self, make_case_study, organization, provider):
        make_case_study(organizations=[provider])
        assert case_studies_for_organization(organization)["received"] == []

    def test_a_deleted_case_study_drops_out(
        self, make_case_study, organization, delete
    ):
        case_study = make_case_study(organizations=[organization])
        delete(case_study)
        assert case_studies_for_organization(organization)["received"] == []
