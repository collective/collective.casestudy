# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0b1 (2025-09-03)


### New features:

- Update Spanish translation @macagua 


### Bug fixes:

- Fix duplication of plone.app.querystring.field.country querystring. @ericof [#9](https://github.com/collective/collective.casestudy/issues/9)
- Fix name of plone.app.querystring.field.versions querystring. @ericof [#10](https://github.com/collective/collective.casestudy/issues/10)
- Fix name of plone.app.querystring.field.usages querystring. @ericof [#11](https://github.com/collective/collective.casestudy/issues/11)
- Fix bug with industries and services tags @instification 


### Internal:

- Refactor GHA support @ericof 
- Replace `pkg_resources` with `pkgutil`. @ericof 
- Use pyproject.toml instead of setup.py. @ericof 

## 1.0.0a3 (2023-06-01)

- Add Provider content type #2 [ericof]

- Add Providers behavior [ericof]

- Add catalog indexes for providers, country, services [ericof]

- Update pt_BR translation [ericof]


## 1.0.0a2 (2023-05-15)

- Added Spanish translation [macagua]

- Use `pytest-plone` for testing.
  [ericof]


## 1.0.0a1 (2022-12-06)

- Initial release. [ericof]
