"""Every profile file is well-formed XML.

Cheap, and it earns its place: GenericSetup parses these at install time, so
a stray `&` in a title does not fail one record -- it aborts the import and
the site comes up half-configured. The symptom is nothing like the cause: a
REST API call returning 400 on an unrelated content type, or a workflow that
was never bound.
"""

from lxml import etree
from pathlib import Path

import collective.casestudy
import pytest


PROFILES = Path(collective.casestudy.__file__).parent / "profiles"

XML_FILES = sorted(PROFILES.rglob("*.xml"))


def _relative(path: Path) -> str:
    return str(path.relative_to(PROFILES))


def test_profiles_folder_found():
    """Guard the glob, so an empty parametrize cannot pass silently."""
    assert len(XML_FILES) > 5


@pytest.mark.parametrize("path", XML_FILES, ids=_relative)
def test_xml_is_well_formed(path: Path):
    """A file GenericSetup cannot parse takes the whole profile with it."""
    try:
        etree.fromstring(path.read_bytes())
    except etree.XMLSyntaxError as exc:  # pragma: no cover - failure path
        pytest.fail(f"{_relative(path)} is not well-formed XML: {exc}")
