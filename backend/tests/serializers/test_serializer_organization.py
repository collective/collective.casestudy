"""The Organization serializers.

``ISerializeToJson`` adds the case studies an organization takes part in, and
``ISerializeToJsonSummary`` adds its social links so a listing can render them
without fetching the object.
"""

from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter

import pytest


class TestOrganizationSerializer:
    """The full ``ISerializeToJson`` representation."""

    def test_case_studies_present(self, organization, serialize):
        """The key is always there, even with nothing related."""
        data = serialize(organization)
        assert data["case_studies"] == {"provided": [], "received": []}

    def test_received_lists_case_studies_about_the_organization(
        self, organization, case_study, relate, serialize
    ):
        """A case study pointing at the organization is one it *received*."""
        relate(case_study, organization, "organizations")
        data = serialize(organization)
        received = data["case_studies"]["received"]
        assert len(received) == 1
        assert received[0]["title"] == case_study.title
        assert data["case_studies"]["provided"] == []

    def test_provided_lists_case_studies_delivered_by_the_organization(
        self, provider, case_study, relate, serialize
    ):
        """A case study naming the organization as a provider is one it *provided*."""
        relate(case_study, provider, "providers")
        data = serialize(provider)
        provided = data["case_studies"]["provided"]
        assert len(provided) == 1
        assert provided[0]["title"] == case_study.title
        assert data["case_studies"]["received"] == []

    def test_both_relations_on_the_same_organization(
        self, provider, case_study, other_case_study, relate, serialize
    ):
        """An organization can provide one case study and be the subject of another."""
        relate(case_study, provider, "providers")
        relate(other_case_study, provider, "organizations")
        data = serialize(provider)
        assert [item["title"] for item in data["case_studies"]["provided"]] == [
            case_study.title
        ]
        assert [item["title"] for item in data["case_studies"]["received"]] == [
            other_case_study.title
        ]

    def test_several_case_studies_in_one_bucket(
        self, organization, case_study, other_case_study, relate, serialize
    ):
        """Every relation of the same kind lands in the same list."""
        relate(case_study, organization, "organizations")
        relate(other_case_study, organization, "organizations")
        data = serialize(organization)
        titles = {item["title"] for item in data["case_studies"]["received"]}
        assert titles == {case_study.title, other_case_study.title}

    def test_relation_to_another_organization_is_not_reported(
        self, organization, provider, case_study, relate, serialize
    ):
        """Relations are looked up by target, so neighbours do not leak in."""
        relate(case_study, provider, "organizations")
        data = serialize(organization)
        assert data["case_studies"]["received"] == []

    @pytest.mark.parametrize(
        "key",
        ["@id", "@type", "title", "description", "review_state"],
    )
    def test_entries_are_summaries(
        self, organization, case_study, relate, serialize, key: str
    ):
        """Case studies are serialized as summaries, not as full objects."""
        relate(case_study, organization, "organizations")
        entry = serialize(organization)["case_studies"]["received"][0]
        assert key in entry

    def test_entries_carry_no_blocks(self, organization, case_study, relate, serialize):
        """A summary is the point: the case study's blocks are not inlined."""
        relate(case_study, organization, "organizations")
        entry = serialize(organization)["case_studies"]["received"][0]
        assert "blocks" not in entry

    def test_broken_relation_is_skipped(
        self, organization, case_study, relate, serialize
    ):
        """A deleted case study drops out instead of raising."""
        relate(case_study, organization, "organizations")
        with api.env.adopt_roles(["Manager"]):
            api.content.delete(obj=case_study, check_linkintegrity=False)
        data = serialize(organization)
        assert data["case_studies"]["received"] == []

    def test_standard_fields_still_serialized(self, organization, serialize):
        """Adding a key must not cost the inherited representation."""
        data = serialize(organization)
        assert data["@type"] == "Organization"
        assert data["title"] == organization.title
        assert data["organization_size"]["token"] == "small"  # noQA: S105


class TestOrganizationSummarySerializer:
    """The ``ISerializeToJsonSummary`` representation of an Organization."""

    def test_social_links_present(self, organization, serialize_summary):
        """Listings render the social links, so the summary carries them."""
        data = serialize_summary(organization)
        assert "social_links" in data

    def test_social_links_value(self, organization, serialize_summary):
        """An organization with no links serializes the field's default."""
        data = serialize_summary(organization)
        assert data["social_links"] in ([], None)

    def test_social_links_round_trip(self, organization, serialize_summary):
        """Whatever is stored on the object is what the summary reports."""
        links = [{"id": "website", "href": [{"@id": "https://ngo1.org"}]}]
        organization.social_links = links
        data = serialize_summary(organization)
        assert data["social_links"] == links

    @pytest.mark.parametrize("key", ["@id", "@type", "title", "description"])
    def test_default_summary_fields_kept(
        self, organization, serialize_summary, key: str
    ):
        """The subclass adds a key; it does not replace the default ones."""
        data = serialize_summary(organization)
        assert key in data

    def test_case_study_summary_has_no_social_links(
        self, case_study, serialize_summary
    ):
        """The adapter is registered for Organization only."""
        data = serialize_summary(case_study)
        assert "social_links" not in data


class TestOrganizationSerializerContract:
    """What the serializer must keep doing because it replaces the default one.

    Organization is a ``Container``, and the adapter registered for
    ``IOrganization`` wins over the folderish one plone.restapi ships -- so
    everything that one contributes has to come from here.
    """

    @pytest.fixture
    def serializer(self, organization, http_request):
        """The ``ISerializeToJson`` adapter itself, for calls with arguments."""
        return getMultiAdapter((organization, http_request), ISerializeToJson)

    def test_is_folderish(self, serializer):
        """An Organization can hold files and images, and says so."""
        assert serializer()["is_folderish"] is True

    def test_items_included_by_default(self, serializer):
        """Folder contents are part of the default representation."""
        data = serializer()
        assert "items" in data
        assert "items_total" in data

    def test_items_can_be_omitted(self, serializer):
        """``include_items=False`` is honoured, as on any folderish content."""
        data = serializer(include_items=False)
        assert "items" not in data

    def test_include_expansion_accepted(self, serializer):
        """The ``@navroot`` endpoint calls with this keyword; it must not raise."""
        data = serializer(include_items=False, include_expansion=False)
        assert "@components" not in data

    def test_case_studies_survive_every_call_shape(self, serializer):
        """The added key does not depend on the arguments."""
        for kwargs in ({}, {"include_items": False}, {"include_expansion": False}):
            assert "case_studies" in serializer(**kwargs)


class TestWorkflowStates:
    """The ``workflow_states`` key the frontend reads.

    ``review_state`` reports the publication workflow only. An additional
    workflow keeps its state under its own variable, which no standard key
    exposes -- so a client cannot tell a verified provider from a draft one
    without this.
    """

    def test_key_is_present(self, organization, serialize):
        assert "workflow_states" in serialize(organization)

    def test_it_reports_every_workflow_in_the_chain(self, organization, serialize):
        """Not only the additional one -- the publication state is here too."""
        assert serialize(organization)["workflow_states"] == {
            "simple_publication_workflow": "private",
        }

    def test_plain_organization_has_no_provider_state(self, organization, serialize):
        """The workflow only joins the chain for a provider."""
        assert "provider_workflow" not in serialize(organization)["workflow_states"]

    def test_provider_reports_the_initial_state(self, provider, serialize):
        states = serialize(provider)["workflow_states"]
        assert states["provider_workflow"] == "created"

    def test_it_follows_a_transition(self, provider, serialize):
        api.content.transition(obj=provider, transition="verify")
        states = serialize(provider)["workflow_states"]
        assert states["provider_workflow"] == "verified"

    def test_it_is_json_serializable(self, provider, serialize):
        """The value is dumped into a REST response, not read in Python."""
        import json

        json.dumps(serialize(provider)["workflow_states"])
