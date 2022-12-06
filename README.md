<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/collective/collective.casestudy/main/docs/icon.svg" width="70" /></div>

<h1 align="center">A Case Study content type for Plone</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.casestudy)](https://pypi.org/project/collective.casestudy/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.casestudy)](https://pypi.org/project/collective.casestudy/)

[![Code analysis checks](https://github.com/collective/collective.casestudy/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/collective/collective.casestudy/actions/workflows/code-analysis.yml)
[![Tests](https://github.com/collective/collective.casestudy/actions/workflows/tests.yaml/badge.svg)](https://github.com/collective/collective.casestudy/actions/workflows/tests.yaml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.casestudy)](https://github.com/collective/collective.casestudy)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.casestudy?style=social)](https://github.com/collective/collective.casestudy)

</div>

Features
--------

**collective.casestudy** provides a Case Study content type to be used in Plone sites.

Documentation
-------------

This package supports Plone sites using Volto, but each project should provide their own view for this content type.


Installation
------------

Add **collective.casestudy** to the Plone installation using `pip`:

```bash
pip install collective.casestudy
```
or add it as a dependency on your package's `setup.py`

```python
    install_requires = [
        "collective.casestudy",
        "Plone",
        "plone.restapi",
        "setuptools",
    ],
```

Start Plone and activate the plugin in the addons control-panel.


Source Code and Contributions
-----------------------------

If you want to help with the development (improvement, update, bug-fixing, ...) of `collective.casestudy` this is a great idea!

- [Issue Tracker](https://github.com/collective/collective.casestudy/issues)
- [Source Code](https://github.com/collective/collective.casestudy/)


We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.

Development
-----------

You need a working `python` environment (system, virtualenv, pyenv, etc) version 3.7 or superior.

Then install the dependencies and a development instance using:

```bash
make build
```

To run tests for this package:

```bash
make test
```

By default we use the latest Plone version in the 6.x series.

License
-------

The project is licensed under the GPLv2.
