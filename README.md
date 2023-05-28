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

## Features

`collective.casestudy` provides two new content types to be used in Plone sites, Case Study and Provider.

### Case Study

A case study of a Plone deployment, which has attributes to track the Plone version used, the industry, and the type of usage of Plone.

### Provider

A company providing Plone services and solutions.

## See it in action

**collective.casestudy** is being used in the following sites:

* [Plone.org](https://plone.org)
* [Plone Brasil](https://plone.org.br)

## Documentation

This package supports Plone sites using Volto, but each project should provide its view for this content type.


### Installation

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


## Source Code and Contributions

We welcome contributions to `collective.casestudy`.
You can create an issue in the issue tracker, or contact a maintainer.

- [Issue Tracker](https://github.com/collective/collective.casestudy/issues)
- [Source Code](https://github.com/collective/collective.casestudy/)



### Development

You need a working Python environment version 3.7 or later.

Then install the dependencies and a development instance using:

```bash
make build
```

By default, we use the latest Plone version in the 6.x series.

## License

The project is licensed under GPLv2.
