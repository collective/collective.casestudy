"""Moving the vocabulary records from strings to objects.

Up to profile version 2000 each vocabulary record held a list of
``"token|title"`` strings -- or, for ``versions``, a bare token whose title was
derived as ``Plone <token>``. From 2100 every record holds an ordered array of
``{"token": ..., "title": ...}``.

The rewrite reads whatever a site actually stores rather than assuming it
matches what this package shipped: a site is free to have added its own terms,
and a term that is already an object -- because the profile was reimported
before this step ran -- is left alone.
"""

from collective.casestudy import logger
from collective.casestudy.interfaces import ICaseStudySettings
from collective.casestudy.vocabularies.terms import term_from_record
from plone import api
from plone.registry.interfaces import IRegistry
from Products.GenericSetup.tool import SetupTool
from zope.component import getUtility


#: Prefix every record of this package is stored under.
PREFIX = "casestudy"

#: Records rewritten by this upgrade. Every one of them existed before 2100,
#: holding ``token|title`` strings.
RECORD_NAMES: tuple[str, ...] = ("industries", "usages", "versions", "services")

#: Record this upgrade *creates*. The size buckets were a constant in code
#: until 2100, so no site can hold a value of its own and there is nothing to
#: convert -- but leaving it empty would give the ``organization_size`` field
#: no terms at all, and an editor could not save an organization.
NEW_RECORD = "organization_sizes"

#: The buckets as of 2100. A snapshot rather than an import from the
#: vocabulary module: an upgrade encodes what was true at its own version, so
#: a later release adding a bucket must not change what this step writes.
NEW_RECORD_TERMS: tuple[tuple[str, str], ...] = (
    ("me", "Just me"),
    ("small", "Up to 5 employees"),
    ("medium", "5 to 30 employees"),
    ("large", "More than 30 employees"),
)

#: Record whose entries carried no title at all, only a version number.
DERIVED_TITLE_RECORD = "versions"


def _title_for(name: str, token: str, title: str) -> str:
    """Return the title to store for one term.

    ``versions`` entries were bare tokens, so their title was never stored;
    it was built for display. This is where that display form becomes data.

    :param name: Record the term belongs to.
    :param token: The term's token.
    :param title: Title read from the stored entry, equal to the token when
        the entry carried none.
    :returns: The title to store.
    """
    if name == DERIVED_TITLE_RECORD and title == token:
        return f"Plone {token}"
    return title


def upgrade_vocabulary_records(context: SetupTool) -> None:
    """Rewrite every vocabulary record as an array of term objects.

    Read, re-register, write -- in that order, and all three here rather than
    leaning on the profile's ``plone.app.registry`` import step. Changing a
    record's field **resets its value**: re-registering the schema first would
    empty every record before this step could read it, and a site's own terms
    would be gone with no way to tell they had ever existed.

    :param context: The setup tool running the upgrade step. Unused.
    """
    registry = getUtility(IRegistry)

    stored = {
        name: api.portal.get_registry_record(f"{PREFIX}.{name}", default=None) or []
        for name in RECORD_NAMES
    }

    # Swaps each record's field from List(TextLine) to JSONField, and empties
    # it -- which is why everything was read above.
    registry.registerInterface(ICaseStudySettings, prefix=PREFIX)

    for name in RECORD_NAMES:
        key = f"{PREFIX}.{name}"
        current = stored[name]
        terms = []
        for entry in current:
            pair = term_from_record(entry)
            if pair is None:
                logger.warning(f"-- {key}: dropping unusable entry {entry!r}")
                continue
            token, title = pair
            terms.append({"token": token, "title": _title_for(name, token, title)})
        api.portal.set_registry_record(key, terms)
        logger.info(f"-- {key}: rewrote {len(terms)} of {len(current)} entries")

    seed_new_record()
    logger.info("Upgrade concluded")


def seed_new_record() -> None:
    """Fill the new ``organization_sizes`` record, unless a value is already there.

    Guarded rather than unconditional so re-running the step, or running it
    after the profile has been reimported, does not overwrite what a site has
    since edited.
    """
    key = f"{PREFIX}.{NEW_RECORD}"
    if api.portal.get_registry_record(key, default=None):
        logger.info(f"-- {key}: left alone, it already has terms")
        return
    terms = [{"token": token, "title": title} for token, title in NEW_RECORD_TERMS]
    api.portal.set_registry_record(key, terms)
    logger.info(f"-- {key}: seeded {len(terms)} entries")
