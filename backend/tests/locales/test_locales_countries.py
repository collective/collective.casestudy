from collective.casestudy import COUNTRIES_DOMAIN
from collective.casestudy.locales import __main__ as locales
from pathlib import Path
from pythongettext.msgfmt import Msgfmt

import gettext
import pycountry
import pytest


class TestSyncCountries:
    """Country names are copied from pycountry into this package's catalogs."""

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path, monkeypatch):
        for lang in ("pt_BR", "es", "xx"):
            (tmp_path / lang / "LC_MESSAGES").mkdir(parents=True)
        monkeypatch.setattr(locales, "locale_path", tmp_path)
        self.path = tmp_path
        locales._sync_countries()

    def _catalog(self, lang: str) -> gettext.GNUTranslations:
        """Compile and load the synced catalog with the compiler Zope uses."""
        po = self.path / lang / "LC_MESSAGES" / f"{COUNTRIES_DOMAIN}.po"
        with po.open("rb") as fp:
            return gettext.GNUTranslations(Msgfmt(fp, COUNTRIES_DOMAIN).getAsFile())

    def test_template_lists_every_country(self):
        pot = self.path / f"{COUNTRIES_DOMAIN}.pot"
        content = pot.read_text(encoding="utf-8")
        assert content.count('\nmsgid "') == len(pycountry.countries)

    @pytest.mark.parametrize(
        "lang,name,expected",
        [
            ("pt_BR", "Brazil", "Brasil"),
            ("pt_BR", "Côte d'Ivoire", "Costa do Marfim"),
            ("es", "Germany", "Alemania"),
        ],
    )
    def test_names_are_translated(self, lang: str, name: str, expected: str):
        assert self._catalog(lang).gettext(name) == expected

    def test_only_country_names_are_copied(self):
        """pycountry's catalog also holds official names; ours must not."""
        catalog = self._catalog("pt_BR")
        assert catalog.gettext("Federative Republic of Brazil") == (
            "Federative Republic of Brazil"
        )

    def test_language_unknown_to_pycountry_is_skipped(self):
        assert not (
            self.path / "xx" / "LC_MESSAGES" / f"{COUNTRIES_DOMAIN}.po"
        ).exists()

    def test_sync_is_stable(self):
        """A second run writes the same bytes, so it never adds noise to a diff."""
        po: Path = self.path / "pt_BR" / "LC_MESSAGES" / f"{COUNTRIES_DOMAIN}.po"
        before = po.read_bytes()
        locales._sync_countries()
        assert po.read_bytes() == before


def test_countries_domain_is_not_rebuilt_by_i18ndude():
    """i18ndude finds none of these runtime messages and would empty the catalogs."""
    assert COUNTRIES_DOMAIN not in locales.domains
