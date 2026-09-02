"""Test layers for this package."""

from OFS.Application import Application
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING
from Products.CMFPlone.Portal import PloneSite

import collective.casestudy


class CaseStudyLayer(PloneSandboxLayer):
    """A Plone site with this package's default profile applied."""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app: Application, configurationContext) -> None:
        """Load this package's ZCML.

        :param app: The Zope application root.
        :param configurationContext: ZCML configuration context.
        """
        self.loadZCML(package=collective.casestudy)

    def setUpPloneSite(self, portal: PloneSite) -> None:
        """Install the package into the test site.

        :param portal: The Plone site.
        """
        applyProfile(portal, "collective.casestudy:default")


FIXTURE = CaseStudyLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="CaseStudyLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, PLONE_RESTAPI_DX_FUNCTIONAL_TESTING),
    name="CaseStudyLayer:FunctionalTesting",
)
