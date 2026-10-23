"""Update locales."""

from collective.casestudy import COUNTRIES_DOMAIN
from pathlib import Path

import gettext
import logging
import pycountry
import re
import subprocess


logger = logging.getLogger("i18n")
logger.setLevel(logging.DEBUG)


PATTERN = r"^[a-z]{2}.*"

locale_path = Path(__file__).parent.resolve()
target_path = locale_path.parent.resolve()
#: Suffix of a pot file listing messages no extractor finds -- i18ndude reads
#: only ``title`` and ``description`` from ZCML, so a ``label`` attribute is
#: listed by hand. It is merged into its domain's pot file on every rebuild.
MANUAL_SUFFIX = "-manual"
#: pycountry's gettext domain for the ISO 3166-1 country names.
PYCOUNTRY_DOMAIN = "iso3166-1"

# The countries domain is left out: its messages are built at runtime from
# pycountry, so i18ndude would extract none of them and empty its catalogs.
domains = [
    path.stem
    for path in locale_path.glob("*.pot")
    if not path.stem.endswith(MANUAL_SUFFIX) and path.stem != COUNTRIES_DOMAIN
]

PO_HEADER = """msgid ""
msgstr ""
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=1; plural=0\\n"
"Language: {lang}\\n"
"Domain: {domain}\\n"
"""

i18ndude = "uvx i18ndude"

# ignore node_modules files resulting in errors
excludes = '"*.html *json-schema*.xml"'


def locale_folder_setup(domain: str):
    languages = [path for path in locale_path.glob("*") if path.is_dir()]
    for lang_folder in languages:
        lc_messages_path = lang_folder / "LC_MESSAGES"
        lang = lang_folder.name
        if lc_messages_path.exists():
            continue
        elif re.match(PATTERN, lang):
            lc_messages_path.mkdir()
            cmd = (
                f"msginit --locale={lang} "
                f"--input={locale_path}/{domain}.pot "
                f"--output={locale_path}/{lang}/LC_MESSAGES/{domain}.po"
            )
            subprocess.call(cmd, shell=True)  # noQA: S602


def _rebuild(domain: str):
    manual = locale_path / f"{domain}{MANUAL_SUFFIX}.pot"
    merge = f"--merge {manual} " if manual.exists() else ""
    cmd = (
        f"{i18ndude} rebuild-pot --pot {locale_path}/{domain}.pot "
        f"{merge}"
        f"--exclude {excludes} "
        f"--create {domain} {target_path}"
    )
    subprocess.call(cmd, shell=True)  # noQA: S602


def _sync(domain: str):
    cmd = (
        f"{i18ndude} sync --pot {locale_path}/{domain}.pot "
        f"{locale_path}/*/LC_MESSAGES/{domain}.po"
    )
    subprocess.call(cmd, shell=True)  # noQA: S602


def _quote(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _write_catalog(path: Path, lang: str, entries: list[tuple[str, str]]):
    """Write a gettext catalog for the countries domain.

    :param path: The ``.po`` or ``.pot`` file to write.
    :param lang: Language code for the header, empty for a template.
    :param entries: ``(msgid, msgstr)`` pairs, in the order to write them.
    """
    blocks = [PO_HEADER.format(lang=lang, domain=COUNTRIES_DOMAIN)]
    for msgid, msgstr in entries:
        blocks.append(f'\nmsgid "{_quote(msgid)}"\nmsgstr "{_quote(msgstr)}"\n')
    path.write_text("".join(blocks), encoding="utf-8")


def _sync_countries():
    """Copy the country names from pycountry's catalogs into ours.

    Only the languages this package already has a folder for are synced, and
    only the names the vocabularies use (``country.name``), not the official or
    common names pycountry's catalog also holds. A name pycountry leaves
    untranslated gets an empty ``msgstr``, so it falls back to English.
    """
    names = sorted(country.name for country in pycountry.countries)
    template = locale_path / f"{COUNTRIES_DOMAIN}.pot"
    _write_catalog(template, "", [(name, "") for name in names])
    for lc_messages_path in sorted(locale_path.glob("*/LC_MESSAGES")):
        lang = lc_messages_path.parent.name
        try:
            translation = gettext.translation(
                PYCOUNTRY_DOMAIN, pycountry.LOCALES_DIR, [lang]
            )
        except FileNotFoundError:
            logger.warning(f"pycountry has no country names for {lang}, skipping")
            continue
        entries = []
        for name in names:
            translated = translation.gettext(name)
            entries.append((name, "" if translated == name else translated))
        _write_catalog(lc_messages_path / f"{COUNTRIES_DOMAIN}.po", lang, entries)


def main():
    for domain in domains:
        logger.info(f"Updating translations for {domain}")
        locale_folder_setup(domain)
        _rebuild(domain)
        _sync(domain)
    logger.info(f"Updating translations for {COUNTRIES_DOMAIN}")
    _sync_countries()


if __name__ == "__main__":
    main()
