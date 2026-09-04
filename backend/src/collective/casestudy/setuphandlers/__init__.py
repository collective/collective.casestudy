"""What the site-creation form and the add-ons control panel must not offer.

The uninstall profile and the upgrades package are implementation details of
this add-on: both would appear as installable products otherwise, and
applying either by hand leaves a site in a state nothing supports.
"""

from plone.base.interfaces.installable import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    """Hide this package's internal profiles and products."""

    def getNonInstallableProfiles(self) -> list[str]:
        """Hide uninstall profile from site-creation and quickinstaller.

        :returns: Profile ids to hide.
        """
        return [
            "collective.casestudy:uninstall",
        ]

    def getNonInstallableProducts(self) -> list[str]:
        """Hide the upgrades package from site-creation and quickinstaller.

        :returns: Product names to hide.
        """
        return [
            "collective.casestudy.upgrades",
        ]
