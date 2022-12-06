from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import collective.casestudy


class CaseStudyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.casestudy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.casestudy:default")


CASESTUDY_FIXTURE = CaseStudyLayer()


CASESTUDY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CASESTUDY_FIXTURE,),
    name="CaseStudyLayer:IntegrationTesting",
)
