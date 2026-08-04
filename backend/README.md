<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/collective/collective.casestudy/main/docs/docs/_static/icon.svg" width="70" /></div>

<h1 align="center">Case Study for Plone</h1>
<h2 align="center">Showcase Plone usage with case studies</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.casestudy)](https://pypi.org/project/collective.casestudy/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.casestudy)](https://pypi.org/project/collective.casestudy/)

[![CI](https://github.com/collective/collective.casestudy/actions/workflows/main.yml/badge.svg)](https://github.com/collective/collective.casestudy/actions/workflows/main.yml)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.casestudy)](https://github.com/collective/collective.casestudy)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.casestudy?style=social)](https://github.com/collective/collective.casestudy)

</div>

The backend package for Case Study for Plone — a Plone 6 add-on that provides content types to be used in Plone sites. See also the frontend package [@plone-collective/volto-casestudy](https://www.npmjs.com/package/@plone-collective/volto-casestudy).

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

This package supports Plone sites using Volto, and you should install the frontend package [@plone-collective/volto-casestudy](https://www.npmjs.com/package/@plone-collective/volto-casestudy) in your project.


### Installation

Add **collective.casestudy** to the Plone installation using `uv`:

```shell
uv add collective.casestudy
```
or add it as a dependency on your project package's `pyproject.toml`

```toml
    dependencies = [
        ...
        "collective.casestudy",
    ],
```

Start Plone and activate the plugin in the addons control-panel.


## Source Code and Contributions

We welcome contributions to `collective.casestudy`.
You can create an issue in the issue tracker, or contact a maintainer.

- [Issue Tracker](https://github.com/collective/collective.casestudy/issues)
- [Source Code](https://github.com/collective/collective.casestudy/)


### Development

You need a working Python environment version 3.10 or later.

Then install the dependencies and a development instance using:

```bash
make install
```

By default, we use the latest Plone version in the 6.x series.

## License

The project is licensed under GPLv2.

## Credits and acknowledgements 🙏

Generated using [Cookieplone (2.0.0b3)](https://github.com/plone/cookieplone) and [cookieplone-templates (f4f4d41)](https://github.com/plone/cookieplone-templates/commit/f4f4d415d32271d41fb87d374b0f807767c1f1b3) on 2026-08-04 12:41:09.957188. A special thanks to all contributors and supporters!
