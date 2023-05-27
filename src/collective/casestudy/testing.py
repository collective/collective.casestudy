from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING

import collective.casestudy


class CaseStudyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.casestudy)

    def setUpPloneSite(self, portal):
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
