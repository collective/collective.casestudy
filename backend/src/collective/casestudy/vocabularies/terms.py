"""Turning a settings record into a vocabulary.

The four vocabulary records all hold the same thing -- an ordered array of
``{"token": ..., "title": ...}`` -- so they all build a vocabulary the same
way, and that way lives here rather than four times over.

Two shapes are accepted. The one the schema declares, and the ``"token|title"``
string a site carried before profile version 2100: a site that has not run the
upgrade yet still gets a working form instead of a traceback from a vocabulary
that every edit form and every listing looks up.
"""

from collective.casestudy import logger
from plone import api
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


#: Separator of the pre-2100 ``token|title`` form.
LEGACY_SEPARATOR = "|"


def term_from_record(entry: dict | str) -> tuple[str, str] | None:
    """Read one settings entry as a ``(token, title)`` pair.

    :param entry: An entry of a vocabulary record, in either the current
        object form or the pre-2100 string form.
    :returns: The pair, or ``None`` when the entry carries no usable token.
    """
    if isinstance(entry, dict):
        token = entry.get("token") or ""
        return (token, entry.get("title") or token) if token else None

    if isinstance(entry, str):
        # Pre-2100: "token|title", or a bare token used as its own title.
        token, _, title = entry.partition(LEGACY_SEPARATOR)
        return (token, title or token) if token else None

    return None


def vocabulary_from_record(name: str) -> SimpleVocabulary:
    """Build a vocabulary from one of this package's settings records.

    Entries are offered in the order the record holds them, which is the
    order the control panel shows and an editor arranges.

    :param name: Registry record name, without the ``casestudy.`` prefix.
    :returns: One term per usable entry.
    """
    record = api.portal.get_registry_record(f"casestudy.{name}") or []
    terms = []
    for entry in record:
        pair = term_from_record(entry)
        if pair is None:
            logger.warning(f"Ignoring unusable entry in casestudy.{name}: {entry!r}")
            continue
        token, title = pair
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
