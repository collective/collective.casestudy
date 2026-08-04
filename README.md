<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/collective/collective.casestudy/main/docs/docs/_static/icon.svg" width="70" /></div>

<h1 align="center">Case Study for Plone</h1>
<h2 align="center">Showcase Plone usage with case studies</h1>

<div align="center">

[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookieplone-0083be.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)

[![PyPI](https://img.shields.io/pypi/v/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.casestudy)](https://pypi.org/project/collective.casestudy/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.casestudy)](https://pypi.org/project/collective.casestudy/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.casestudy)](https://pypi.org/project/collective.casestudy/)

[![npm](https://img.shields.io/npm/v/@plone-collective/volto-casestudy)](https://www.npmjs.com/package/@plone-collective/volto-casestudy)
[![](https://img.shields.io/badge/-Storybook-ff4785?logo=Storybook&logoColor=white&style=flat-square)](https://kitconcept.github.io/kitconcept-keywordmanager/)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.casestudy)](https://github.com/collective/collective.casestudy)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.casestudy?style=social)](https://github.com/collective/collective.casestudy)

[![CI](https://github.com/collective/collective.casestudy/actions/workflows/main.yml/badge.svg)](https://github.com/collective/collective.casestudy/actions/workflows/main.yml)

</div>

## Quick Start 🏁

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [nvm](https://6.docs.plone.org/install/create-project-cookieplone.html#nvm)
-   [Node.js and pnpm](https://6.docs.plone.org/install/create-project.html#node-js) 24
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)


### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:collective/collective.casestudy.git
    cd collective.casestudy
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Fire Up the Servers 🔥

1.  Create a new Plone site on your first run.

    ```shell
    make backend-create-site
    ```

2.  Start the backend at http://localhost:8080/.

    ```shell
    make backend-start
    ```

3.  In a new shell session, start the frontend at http://localhost:3000/.

    ```shell
    make frontend-start
    ```

Voila! Your Plone site should be live and kicking! 🎉

### Local Stack Deployment 📦

Deploy a local Docker Compose environment that includes the following.

- Docker images for Backend and Frontend 🖼️
- A stack with a Traefik router and a PostgreSQL database 🗃️
- Accessible at [http://collective.casestudy.localhost](http://collective.casestudy.localhost) 🌐

Run the following commands in a shell session.

```shell
make stack-create-site
make stack-start
```

And... you're all set! Your Plone site is up and running locally! 🚀

## Project structure 🏗️

This monorepo consists of the following distinct sections:

- **backend**: Houses the API and Plone installation, utilizing pip instead of buildout, and includes a policy package named collective.casestudy.
- **frontend**: Contains the React (Volto) package.
- **devops**: Encompasses Docker stack, Ansible playbooks, and cache settings.
- **docs**: Scaffold for writing documentation for your project.

### Why this structure? 🤔

- All necessary codebases to run the site are contained within the repository (excluding existing add-ons for Plone and React).
- Specific GitHub Workflows are triggered based on changes in each codebase (refer to .github/workflows).
- Simplifies the creation of Docker images for each codebase.
- Demonstrates Plone installation/setup without buildout.

## Code quality assurance 🧐

To check your code against quality standards, run the following shell command.

```shell
make check
```

### Format the codebase

To format and rewrite the code base, ensuring it adheres to quality standards, run the following shell command.

```shell
make format
```

| Section | Tool | Description | Configuration |
| --- | --- | --- | --- |
| backend | Ruff | Python code formatting, imports sorting  | [`backend/pyproject.toml`](./backend/pyproject.toml) |
| backend | `zpretty` | XML and ZCML formatting  | -- |
| frontend | ESLint | Fixes most common frontend issues | [`frontend/.eslintrc.js`](.frontend/.eslintrc.js) |
| frontend | prettier | Format JS and Typescript code  | [`frontend/.prettierrc`](.frontend/.prettierrc) |
| frontend | Stylelint | Format Styles (css, less, sass)  | [`frontend/.stylelintrc`](.frontend/.stylelintrc) |

Formatters can also be run within the `backend` or `frontend` folders.

### Linting the codebase
or `lint`:

 ```shell
make lint
```

| Section | Tool | Description | Configuration |
| --- | --- | --- | --- |
| backend | Ruff | Checks code formatting, imports sorting  | [`backend/pyproject.toml`](./backend/pyproject.toml) |
| backend | Pyroma | Checks Python package metadata  | -- |
| backend | check-python-versions | Checks Python version information  | -- |
| backend | `zpretty` | Checks XML and ZCML formatting  | -- |
| frontend | ESLint | Checks JS / Typescript lint | [`frontend/.eslintrc.js`](.frontend/.eslintrc.js) |
| frontend | prettier | Check JS / Typescript formatting  | [`frontend/.prettierrc`](.frontend/.prettierrc) |
| frontend | Stylelint | Check Styles (css, less, sass) formatting  | [`frontend/.stylelintrc`](.frontend/.stylelintrc) |

Linters can be run individually within the `backend` or `frontend` folders.

## Internationalization 🌐

Generate translation files for Plone and Volto with ease:

```shell
make i18n
```

## Credits and acknowledgements 🙏

Generated using [Cookieplone (2.0.0b3)](https://github.com/plone/cookieplone) and [cookieplone-templates (f4f4d41)](https://github.com/plone/cookieplone-templates/commit/f4f4d415d32271d41fb87d374b0f807767c1f1b3) on 2026-08-04 12:41:09.957188. A special thanks to all contributors and supporters!
