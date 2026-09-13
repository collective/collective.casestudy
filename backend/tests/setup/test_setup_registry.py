from plone import api

import pytest


@pytest.fixture(scope="class")
def portal(portal_class):
    yield portal_class


#: Operations every Yes/No querystring field offers.
BOOLEAN_OPERATIONS = [
    "plone.app.querystring.operation.boolean.isTrue",
    "plone.app.querystring.operation.boolean.isFalse",
]

#: Yes/No querystring fields filtering by listing and verification, and the
#: group each is offered in.
BOOLEAN_FIELDS = {
    "case_study_verified": "Case Studies",
    "case_study_listed": "Case Studies",
    "provider_verified": "Providers",
    "provider_listed": "Providers",
}


class TestRegistryValues:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal

    @pytest.mark.parametrize(
        "field_name,key,expected",
        [
            ("industry", "title", "label_industry"),
            ("industry", "description", "description_qs_industry"),
            ("industry", "enabled", True),
            ("industry", "sortable", False),
            (
                "industry",
                "operations",
                [
                    "plone.app.querystring.operation.selection.any",
                ],
            ),
            ("industry", "vocabulary", "collective.casestudy.vocabulary.industries"),
            ("industry", "group", "Case Studies"),
            ("usages", "title", "label_usage"),
            ("usages", "description", "description_qs_usage"),
            ("usages", "enabled", True),
            ("usages", "sortable", False),
            (
                "usages",
                "operations",
                [
                    "plone.app.querystring.operation.selection.any",
                ],
            ),
            ("usages", "vocabulary", "collective.casestudy.vocabulary.usages"),
            ("usages", "group", "Case Studies"),
            ("versions", "title", "label_version"),
            ("versions", "description", "description_qs_version"),
            ("versions", "enabled", True),
            ("versions", "sortable", False),
            (
                "versions",
                "operations",
                [
                    "plone.app.querystring.operation.selection.any",
                ],
            ),
            ("versions", "vocabulary", "collective.casestudy.vocabulary.versions"),
            ("versions", "group", "Case Studies"),
            ("providers", "title", "label_provider"),
            ("providers", "description", "description_qs_provider"),
            ("providers", "enabled", True),
            ("providers", "sortable", False),
            (
                "providers",
                "operations",
                [
                    "plone.app.querystring.operation.selection.any",
                ],
            ),
            ("providers", "vocabulary", "collective.casestudy.vocabulary.providers"),
            ("providers", "group", "Case Studies"),
            ("facets", "group", "Organizations"),
            ("country", "title", "label_country"),
            ("country", "description", "description_qs_country"),
            ("country", "enabled", True),
            ("country", "sortable", False),
            (
                "country",
                "operations",
                [
                    "plone.app.querystring.operation.selection.any",
                ],
            ),
            ("country", "vocabulary", "collective.casestudy.vocabulary.countries"),
            ("country", "group", "Providers"),
            ("services", "title", "label_services"),
            ("services", "description", "description_qs_services"),
            ("services", "enabled", True),
            ("services", "sortable", False),
            (
                "services",
                "operations",
                [
                    "plone.app.querystring.operation.selection.any",
                ],
            ),
            ("services", "vocabulary", "collective.casestudy.vocabulary.services"),
            ("services", "group", "Providers"),
        ],
    )
    def test_plone_qs_field(self, field_name: str, key: str, expected):
        reg_key = f"plone.app.querystring.field.{field_name}.{key}"
        value = api.portal.get_registry_record(reg_key)
        assert value == expected

    @pytest.mark.parametrize(
        "field_name,key,expected",
        [
            (field_name, key, expected)
            for field_name, group in BOOLEAN_FIELDS.items()
            for key, expected in (
                ("title", f"label_{field_name}"),
                ("description", f"description_qs_{field_name}"),
                ("enabled", True),
                ("sortable", False),
                ("operations", BOOLEAN_OPERATIONS),
                ("group", group),
            )
        ],
    )
    def test_plone_boolean_qs_field(self, field_name: str, key: str, expected):
        reg_key = f"plone.app.querystring.field.{field_name}.{key}"
        value = api.portal.get_registry_record(reg_key)
        assert value == expected

    @pytest.mark.parametrize("field_name", ["usage", "version"])
    def test_plone_old_qs_fields_should_not_be_available(self, field_name: str):
        reg_key = f"plone.app.querystring.field.{field_name}.title"
        with pytest.raises(api.exc.InvalidParameterError) as e:
            api.portal.get_registry_record(reg_key)
        assert str(e.value) == f"Cannot find a record with name '{reg_key}'"
