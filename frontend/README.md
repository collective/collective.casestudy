<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/collective/collective.casestudy/main/docs/docs/_static/icon.svg" width="70" /></div>

<h1 align="center">Case Study for Plone</h1>
<h2 align="center">Showcase Plone usage with case studies</h1>

<div align="center">

[![npm](https://img.shields.io/npm/v/@plone-collective/volto-casestudy)](https://www.npmjs.com/package/@plone-collective/volto-casestudy)
[![](https://img.shields.io/badge/-Storybook-ff4785?logo=Storybook&logoColor=white&style=flat-square)](https://collective.github.io/volto-casestudy/)
[![CI](https://github.com/collective/collective.casestudy/actions/workflows/main.yml/badge.svg)](https://github.com/collective/collective.casestudy/actions/workflows/main.yml)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.casestudy)](https://github.com/collective/collective.casestudy)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.casestudy?style=social)](https://github.com/collective/collective.casestudy)

</div>

The frontend package for Case Study for Plone — a Plone 6 add-on that . See also the backend package [collective.casestudy](https://pypi.org/project/collective.casestudy/).

## Features 🔥

TODO

## Installation

To install your project, you must choose the method appropriate to your version of Volto.


### Volto 18 and later

Add `@plone-collective/volto-casestudy` to your `package.json`.

```json
"addons": [
    ...
    "@plone-collective/volto-casestudy"
],
"dependencies": {
    "@plone-collective/volto-casestudy": "*"
}
```

## Test installation

Visit http://localhost:3000/ in a browser, login, and check the awesome new features.


## Development

The development of this add-on is done in isolation using pnpm workspaces, the latest `mrs-developer`, and other Volto core improvements.
For these reasons, it only works with pnpm and Volto 18.


### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [nvm](https://6.docs.plone.org/install/create-project-cookieplone.html#nvm)
-   [Node.js and pnpm](https://6.docs.plone.org/install/create-project.html#node-js) 24
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:collective/collective.casestudy.git
    cd collective.casestudy/frontend
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Make convenience commands

Run `make help` to list the available Make commands.


### Set up development environment

Install package requirements.

```shell
make install
```

### Start developing

Start the backend.

```shell
make backend-docker-start
```

In a separate terminal session, start the frontend.

```shell
make start
```

### Lint code

Run ESlint, Prettier, and Stylelint in analyze mode.

```shell
make lint
```

### Format code

Run ESlint, Prettier, and Stylelint in fix mode.

```shell
make format
```

### i18n

Extract the i18n messages to locales.

```shell
make i18n
```

### Unit tests

Run unit tests.

```shell
make test
```

### Run Cypress tests

Run each of these steps in separate terminal sessions.

In the first session, start the frontend in development mode.

```shell
make acceptance-frontend-dev-start
```

In the second session, start the backend acceptance server.

```shell
make acceptance-backend-start
```

In the third session, start the Cypress interactive test runner.

```shell
make acceptance-test
```

## Contributing 🐛

Contributions are welcome! Please read [CONTRIBUTING.md](https://github.com/collective/collective.casestudy/blob/main/CONTRIBUTING.md).

## License

The project is licensed under the MIT license.

## Credits and acknowledgements 🙏

Generated using [Cookieplone (2.0.0b3)](https://github.com/plone/cookieplone) and [cookieplone-templates (f4f4d41)](https://github.com/plone/cookieplone-templates/commit/f4f4d415d32271d41fb87d374b0f807767c1f1b3) on 2026-08-04 12:41:09.957188. A special thanks to all contributors and supporters!
