from collective.casestudy.testing import CASESTUDY_INTEGRATION_TESTING

import gocept.pytestlayer.fixture
import pytest


globals().update(
    gocept.pytestlayer.fixture.create(
        CASESTUDY_INTEGRATION_TESTING,
        session_fixture_name="integration_session",
        class_fixture_name="integration_class",
        function_fixture_name="integration",
    )
)


@pytest.fixture
def portal(integration):
    return integration["portal"]


@pytest.fixture
def http_request(integration):
    return integration["request"]
