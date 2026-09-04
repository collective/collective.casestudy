"""The CaseStudy subscribers.

``USER_FACET`` is derived from the case studies pointing at an organization,
so it only becomes true when something reindexes the *organization* -- which
is what these handlers are for.
"""

from collective.casestudy.subscribers.case_study import related_organizations
from collective.casestudy.vocabularies.organization import DEFAULT_FACET
from collective.casestudy.vocabularies.organization import USER_FACET
from plone import api
from zope.lifecycleevent import modified

import pytest


class TestRelatedOrganizations:
    """The lookup the handlers are built on."""

    def test_none_when_the_case_study_names_nobody(self, make_case_study):
        assert related_organizations(make_case_study()) == []

    def test_one_per_relation(self, make_case_study, organization):
        case_study = make_case_study(organizations=[organization])
        assert related_organizations(case_study) == [organization]

    def test_keeps_every_relation(
        self, make_case_study, organization, other_organization
    ):
        case_study = make_case_study(organizations=[organization, other_organization])
        assert len(related_organizations(case_study)) == 2

    def test_skips_a_deleted_organization(self, make_case_study, organization):
        """A relation with nothing behind it has nothing to reindex.

        Following it would raise from an event handler, which turns a stale
        relation into a case study that can no longer be saved.
        """
        case_study = make_case_study(organizations=[organization])
        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=organization, check_linkintegrity=False)
        assert related_organizations(case_study) == []

    def test_survives_the_behavior_being_switched_off(self):
        """`organizations` comes from a behavior a site may have removed.

        A real CaseStudy always answers it -- Dexterity falls back to the
        schema default -- so the attribute has to be taken away to exercise
        the guard at all.
        """

        class WithoutTheBehavior:
            pass

        assert related_organizations(WithoutTheBehavior()) == []

    def test_survives_a_none_value(self, make_case_study):
        """A field explicitly set to None is not an empty list."""
        case_study = make_case_study()
        case_study.organizations = None
        assert related_organizations(case_study) == []


class TestAdded:
    """Creating a case study."""

    def test_organization_starts_without_the_user_facet(self, organization, facets_of):
        assert facets_of(organization) == [DEFAULT_FACET]

    def test_creation_marks_the_organization_as_a_user(
        self, make_case_study, organization, facets_of
    ):
        """The relation catalog is already populated when the add event fires."""
        make_case_study(organizations=[organization])
        assert USER_FACET in facets_of(organization)

    def test_every_named_organization_is_marked(
        self, make_case_study, organization, other_organization, facets_of
    ):
        make_case_study(organizations=[organization, other_organization])
        assert USER_FACET in facets_of(organization)
        assert USER_FACET in facets_of(other_organization)

    def test_an_unrelated_organization_is_untouched(
        self, make_case_study, organization, other_organization, facets_of
    ):
        make_case_study(organizations=[organization])
        assert USER_FACET not in facets_of(other_organization)

    def test_the_default_facet_is_kept(self, make_case_study, organization, facets_of):
        make_case_study(organizations=[organization])
        assert DEFAULT_FACET in facets_of(organization)

    def test_a_case_study_naming_nobody_is_fine(self, make_case_study):
        assert make_case_study() is not None


class TestModified:
    """Editing a case study."""

    def test_relating_an_organization_marks_it(
        self, make_case_study, organization, facets_of
    ):
        case_study = make_case_study()
        assert USER_FACET not in facets_of(organization)

        api.relation.create(
            source=case_study, target=organization, relationship="organizations"
        )
        modified(case_study)
        assert USER_FACET in facets_of(organization)

    def test_adding_a_second_organization_marks_it_too(
        self, make_case_study, organization, other_organization, facets_of
    ):
        case_study = make_case_study(organizations=[organization])
        api.relation.create(
            source=case_study,
            target=other_organization,
            relationship="organizations",
        )
        modified(case_study)
        assert USER_FACET in facets_of(other_organization)
        assert USER_FACET in facets_of(organization)

    def test_a_deleted_organization_does_not_break_the_save(
        self, make_case_study, organization
    ):
        """The regression that made this handler raise: `to_object` is None."""
        case_study = make_case_study(organizations=[organization])
        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=organization, check_linkintegrity=False)
        modified(case_study)

    def test_editing_a_case_study_naming_nobody_is_fine(self, make_case_study):
        modified(make_case_study())


class TestKnownGaps:
    """What the handlers do *not* cover, asserted so nobody has to rediscover it.

    Both are the same shape: the facet is derived, so an organization that
    stops being related has to be reindexed too -- and nothing reindexes it,
    because the handlers only ever look at the relations a case study still
    has.
    """

    @pytest.mark.xfail(
        reason="No handler reindexes an organization that was just unlinked",
        strict=True,
    )
    def test_unlinking_clears_the_user_facet(
        self, make_case_study, organization, facets_of
    ):
        case_study = make_case_study(organizations=[organization])
        assert USER_FACET in facets_of(organization)

        case_study.organizations = []
        modified(case_study)
        assert USER_FACET not in facets_of(organization)

    @pytest.mark.xfail(
        reason="No IObjectRemovedEvent handler for CaseStudy",
        strict=True,
    )
    def test_deleting_the_case_study_clears_the_user_facet(
        self, make_case_study, organization, facets_of
    ):
        case_study = make_case_study(organizations=[organization])
        assert USER_FACET in facets_of(organization)

        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=case_study, check_linkintegrity=False)
        assert USER_FACET not in facets_of(organization)
