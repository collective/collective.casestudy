"""Tests for the querystring fields filtering by listing and verification.

Each field is a Yes/No criterion that an ``IParsedQueryIndexModifier`` utility
of the same name rewrites onto `collective.multiworkflow`'s ``workflow_states``
index, whose values read ``<workflow-id>|<state-id>``.

What *No* means is taken from the modifiers' own docstrings: content that runs
the field's workflow but is not in the matching states. Content that never
runs that workflow -- a plain organization, a document, a case study for a
provider field -- matches neither *Yes* nor *No*.
"""

IS_TRUE = "plone.app.querystring.operation.boolean.isTrue"
IS_FALSE = "plone.app.querystring.operation.boolean.isFalse"
ANY = "plone.app.querystring.operation.selection.any"

CASESTUDY_WORKFLOW = "casestudy_workflow"
PROVIDER_WORKFLOW = "provider_workflow"

#: Querystring field -> the workflow whose states it filters on.
FIELDS: dict[str, str] = {
    "case_study_verified": CASESTUDY_WORKFLOW,
    "case_study_listed": CASESTUDY_WORKFLOW,
    "provider_verified": PROVIDER_WORKFLOW,
    "provider_listed": PROVIDER_WORKFLOW,
}

#: States a *Yes* matches, per kind of field.
VERIFIED_STATES = {"verified"}
LISTED_STATES = {"listed", "verified"}

#: Case studies to create, by id, with the transitions putting each in its state.
CASE_STUDIES: dict[str, list[str]] = {
    "cs-created": [],
    "cs-pending": ["review"],
    "cs-listed": ["list"],
    "cs-verified": ["verify"],
    "cs-archived": ["archive"],
}

#: Providers to create, by id, with their ``provider_workflow`` transitions.
PROVIDERS: dict[str, list[str]] = {
    "pv-created": [],
    "pv-pending": ["review"],
    "pv-listed": ["list"],
    "pv-verified": ["verify"],
    "pv-verified-private": ["verify"],
    "pv-archived": ["archive"],
}

#: An organization that is not a provider, so it never runs ``provider_workflow``.
PLAIN_ORGANIZATION = "org-plain"

#: A document, running neither of the two workflows.
DOCUMENT = "doc-published"

#: Content published through ``simple_publication_workflow``.
#: ``pv-verified-private`` stays private, so a verified provider exists on each
#: side of a ``review_state`` criterion.
PUBLISHED = {"pv-listed", "pv-verified", PLAIN_ORGANIZATION, DOCUMENT}

#: What each field matches, by operation.
EXPECTED: dict[tuple[str, str], set[str]] = {
    ("case_study_verified", IS_TRUE): {"cs-verified"},
    ("case_study_verified", IS_FALSE): {
        "cs-created",
        "cs-pending",
        "cs-listed",
        "cs-archived",
    },
    ("case_study_listed", IS_TRUE): {"cs-listed", "cs-verified"},
    ("case_study_listed", IS_FALSE): {"cs-created", "cs-pending", "cs-archived"},
    ("provider_verified", IS_TRUE): {"pv-verified", "pv-verified-private"},
    ("provider_verified", IS_FALSE): {
        "pv-created",
        "pv-pending",
        "pv-listed",
        "pv-archived",
    },
    ("provider_listed", IS_TRUE): {"pv-listed", "pv-verified", "pv-verified-private"},
    ("provider_listed", IS_FALSE): {"pv-created", "pv-pending", "pv-archived"},
}
