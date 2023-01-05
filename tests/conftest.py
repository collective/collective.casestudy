from collective.casestudy.testing import CASESTUDY_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(fixtures_factory(((CASESTUDY_INTEGRATION_TESTING, "integration"),)))
