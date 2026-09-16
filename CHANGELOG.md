# Change log

<!-- You should *NOT* be adding new change log entries to this file.
     You should create a file in the news directory instead.
     For helpful instructions, please see:
     https://6.docs.plone.org/contributing/index.html#contributing-change-log-label
-->

<!-- towncrier release notes start -->
## 2.0.0a1 (2026-09-16)

### Backend


#### Breaking changes:

- Move the `collective.casestudy` package to the `backend` folder and require Plone 6.2 and Python 3.11 or newer. @ericof [#13](https://github.com/collective/collective.casestudy/issues/13)
- Remove the `Provider` content type in favour of `Organization`, together with its workflow and its add permission. Profile version 2200 removes it from an existing site, but only once no Provider content is left: converting an item is an editorial decision, so the upgrade counts what remains, says which items they are, and changes nothing until they are gone. Run the step again after migrating to finish the removal. @ericof [#15](https://github.com/collective/collective.casestudy/issues/15)
- Make the provider information of an organization staff-only until its listing is approved. The fields used to be readable by anyone, granted through the rolemap; they are now governed by `provider_workflow`, whose `created` and `pending` states do not name `Anonymous`. A provider becomes publicly readable again on `list` or `verify`. Existing content is unaffected until it is edited, because the marker interface that adds the workflow is applied on save. @ericof [#24](https://github.com/collective/collective.casestudy/issues/24)
- Replace `simple_publication_workflow` on case studies with a `casestudy_workflow` of their own. It moves through the same states as `provider_workflow` — `created`, `pending`, `listed`, `verified` and `archived` — and manages the standard `Access contents information`, `View` and `Modify portal content` permissions: a case study is visible to anonymous visitors once it is `listed`, `verified` or `archived`, and only site administrators can edit it once it is verified or archived. Listing, verifying and archiving require `Review portal content`. An upgrade step moves existing case studies onto the new workflow, mapping `private` to `created`, `pending` to `pending` and `published` to `listed`. Queries and listings that filter case studies on the `published` review state no longer match them. @ericof [#26](https://github.com/collective/collective.casestudy/issues/26)
- Require `collective.multiworkflow` 1.0.0a2. The Organization serialization no longer replaces the add-on's `workflow_states` key with a mapping of workflow id to state: like every other content type, it now carries the list of `<workflow-id>|<state-id>` values the add-on serializes, in chain order. REST API clients reading `workflow_states["provider_workflow"]` have to parse the list instead, for example with `collective.multiworkflow.utils.workflow.parse_state`. @ericof 
- Store the industries, usages, versions and services settings as an ordered list of `{token, title}` objects instead of `token|title` strings, and give `versions` the explicit titles it used to derive. Profile version 2100 migrates the values a site already holds, including terms it added itself. Two consequences worth knowing: a title may now contain a `|`, and reimporting the default profile replaces these records rather than merging into them, so a site that customised them should reapply its terms afterwards. @ericof 


#### New features:

- Add an `initial` profile that creates example content to showcase the add-on. @ericof [#13](https://github.com/collective/collective.casestudy/issues/13)
- Add the `Organization` content type, representing any organization in the Plone ecosystem: a Plone user, a solution provider, or both. Provider fields move to a `provider_info` behavior, a `facets` index records which roles an organization plays, and the providers vocabulary lists the organizations flagged as such. The REST API representation of an organization gains a `case_studies` key with the case studies it provided and the ones it is the subject of. @ericof [#15](https://github.com/collective/collective.casestudy/issues/15)
- Track a provider's listing status in its own workflow. `collective.multiworkflow` appends a `provider_workflow` to an organization that opts in through `is_provider`, so the listing decision is separate from publishing the page: an organization moves through `created`, `pending`, `listed`, `verified` and `archived` while its page stays published throughout. The REST API representation of an organization gains a `workflow_states` key reporting the state of every workflow in its chain, because `review_state` only ever describes the publication one. The marker interface that adds the workflow to the chain is applied after the object was created, so the workflow is told the object exists before its role mappings are written: without that it has no status and no creation entry in its history, and DCWorkflow quietly answers a missing status with the workflow's initial state. @ericof [#24](https://github.com/collective/collective.casestudy/issues/24)
- Add Yes/No querystring filters for case studies and providers: `Case Study Listed`, `Case Study Verified`, `Provider Listed` and `Provider Verified`. *Yes* matches content that is listed or verified — or verified only, for the verified filters — and *No* matches the other states of the same workflow; content that does not run that workflow matches neither. The case study filters are now grouped under `Case Studies`, and `Country` and `Services` under `Providers`. An upgrade step brings the new filters and groups to existing sites. The filters are rewritten onto the `workflow_states` index, as `Review state` is, so a query combining two of them keeps only one of the criteria. @ericof [#27](https://github.com/collective/collective.casestudy/issues/27)
- Add a rich text `text` field to the `provider_info` behavior, so a provider can describe itself and its work in formatted text. It is set up like the `plone.richtext` behavior — rich text widget, primary field, searchable — and guarded like `services`: readable by anyone once the provider is listed or verified, and editable by whoever may edit the provider information. @ericof [#28](https://github.com/collective/collective.casestudy/issues/28)
- Make `contact_name` and `contact_email` optional on the `contact_info` behavior. An organization can now publish its address or its industry without naming a person, and the frontend drops the contact block entirely when none of the three fields is set. @ericof [#31](https://github.com/collective/collective.casestudy/issues/31)
- Add `plonegovbr.socialmedia` as a dependency, installing its default profile with the add-on. @ericof 
- Give the Case Study control panel an icon, so it is no longer the only unlabelled tile in the control panel listing. @ericof 
- Keep an organization's facets in step with the case studies about it. The `User` facet is derived from the case studies pointing at an organization, so creating or editing one now reindexes the organizations it names — without that a newly published case study left its organization listed as one nobody had written about. @ericof 
- Name `provider_workflow` "Provider listing" through the `label` attribute of `<plone:additionalworkflows />`. The `@workflow` endpoint, the Volto workflow control and history, and the options of the **Review state** collection criterion show the label in place of the workflow's title. @ericof 
- Report the `providerView` layout for an organization flagged as a provider whose listing is `listed` or `verified`, so Volto renders it with a page of its own. Other organizations keep their layout. @ericof 


#### Bug fixes:

- Skip and log country codes the `country` index holds but `pycountry` cannot resolve, instead of raising from a vocabulary that every listing and edit form looks up. @ericof 
- Skip deleted providers when indexing the `providers` relation. Reindexing a case study whose provider had been removed raised, which also aborted a site-wide catalog rebuild at the first such item. @ericof 


#### Internal:

- Use `plone.autoinclude` instead of `z3c.autoinclude`, hide the uninstall profile and the upgrades package from the quickinstaller, and drop the `zest.releaser` based release tooling. @ericof [#13](https://github.com/collective/collective.casestudy/issues/13)
- Add type annotations and reStructuredText docstrings to the serializers, indexers, vocabularies, setup handlers and upgrade steps. @ericof 
- Import `format_state`, `parse_state` and `WORKFLOW_STATES` from `collective.multiworkflow.utils.workflow`, their location since `collective.multiworkflow` 1.0.0a2, and stop requesting the `workflow_states` summary column, which the add-on now requests itself. @ericof 
- Require `plonegovbr.socialmedia` 3.0.0. It registers `social_links` as a site-wide catalog column and names it for every summary, so the key now rides along on any content summary with an empty value, exactly as `facets` does; the Organization summary serializer remains the only thing that fills it in. @ericof 


#### Tests

- Add test coverage for the provider workflow, including the cases that only arise because an organization runs two workflows at once: the permission sets of the two proven disjoint, each workflow transitioning while the other's role mappings are watched, transition ids proven not to collide, guards that deny rather than merely exist, and each workflow keeping its own history under its own state variable. The workflow definition itself is checked for a state graph that closes — every exit transition defined, every transition targeting a real state, no unreachable transitions and no dead ends — none of which GenericSetup validates at import time. The test layer now loads `collective.multiworkflow`'s `meta.zcml` before this package's ZCML, without which the `plone:additionalworkflows` directive is unknown and every test errors during layer setup. @ericof [#24](https://github.com/collective/collective.casestudy/issues/24)
- Add test coverage for the Organization serializers, the site-wide summary metadata, and the case studies an organization exposes over the REST API, including the permission filtering that hides unpublished ones. @ericof 
- Test that a **Review state** criterion naming no workflow combines with the listing and verification querystring fields, and that the provider workflow's label reaches the `@workflow` endpoint and the review state vocabulary. @ericof 
- Test which roles hold each permission `casestudy_workflow` and `provider_workflow` manage, in every state, for anonymous visitors and users holding each standard role. @ericof 



### Frontend


#### Breaking

- Require `@plone-collective/volto-multiworkflow` 1.0.0-alpha.2. `Organization['workflow_states']` is now the list of `<workflow-id>|<state-id>` values the backend serializes, and `ProviderInfo` reads the verified state from it with the add-on's `getWorkflowStates` and `formatWorkflowState` helpers. @ericof 


#### Feature

- Add the `@plone-collective/volto-casestudy` package, a Volto add-on for the Case Study and Provider content types. @ericof [#13](https://github.com/collective/collective.casestudy/issues/13)
- Add the `Organization` view and the `OrganizationMetadata` block, replacing their `Provider` counterparts, and an `OrganizationLink` component that renders a related organization as its logo or its title. The Case Study metadata block uses it to list the organizations and the providers of a case study. @ericof [#15](https://github.com/collective/collective.casestudy/issues/15)
- Add CaseStudyMetadata block and CaseStudy view @fosten [#18](https://github.com/collective/collective.casestudy/issues/18)
- Show the address and the services of a provider on the organization view, and mark a verified provider with a badge. The block appears only for an organization flagged as a provider, the services list is dropped when there are none, and the badge follows the `provider_workflow` state rather than the publication state. @ericof [#24](https://github.com/collective/collective.casestudy/issues/24)
- Redesign the organization and provider pages. Both now open with a shared `OrganizationHeader` — logo, label, title, description and social links — and render their details through information blocks: address and industry for an organization, address, contact and services for a provider. The case studies move to the foot of the page as a full-width band, split into the ones the organization delivered and the ones it is the subject of. The provider page also renders the `text` field as an About section. @ericof [#31](https://github.com/collective/collective.casestudy/issues/31)
- Give the `provider_workflow` states their own colours in the workflow menu and the history. Volto paints each state from `settings.workflowMapping` and falls back to black for an id it does not know, so `created`, `listed`, `verified` and `archived` — and the transitions that lead to them — are registered there. The keys are site-wide, so a state id of another workflow with the same name is coloured too. @ericof [#32](https://github.com/collective/collective.casestudy/issues/32)
- Add `@plonegovbr/volto-social-media` as an add-on dependency. @ericof 
- Add a `ProviderView`, registered as the `providerView` layout, that renders a listed provider's address, services and verified badge next to its logo, social links and case studies. `OrganizationView` no longer shows provider information. The logo and social links are now the reusable `OrganizationLogo` and `OrganizationSocialLinks` components. @ericof 
- Edit the industries, usages, versions and services settings with a term-by-term widget instead of the raw JSON editor. Each row has a token and a title, and rows can be added, removed and reordered. A site that has not run the 2100 upgrade yet still gets an editable panel: the old `token|title` strings are read and converted on save. @ericof 
- Give the Case Study control panel an icon, matching the one the classic interface shows. @ericof 
- Render the case studies through an `organizationFooter` slot rather than calling the component from each view. The add-on registers `CaseStudies` in that slot behind a `hasCaseStudies` predicate, so a project can add components to the foot of an organization page, reorder them, or replace the listing without shadowing either view. The slot is named for the place, not for what currently fills it. @ericof 


#### Internal

- Give every component a folder of its own, holding its implementation, styles, tests and stories. The information blocks — `AddressInfo`, `ContactInfo`, `IndustryInfo` and `ServicesInfo` — sit under `InfoBlocks`, `CaseStudyGroup` and `CaseStudyEntry` under `CaseStudies`, and each view under `Views/<Name>`. The repeated block rules moved into SCSS mixins shared by the callers, and the values they hardcoded into custom properties in `theme/root.css`. @ericof 
- Keep the monorepo-relative TypeScript paths in `tsconfig.json` and leave that file out of the published package. An IDE reads no other filename, so the paths have to live there; Volto's add-on registry reads a released add-on's `tsconfig.json` and lets its `paths` override the aliases it already resolved, so shipping them would break module resolution for consuming projects. @ericof 


#### Tests

- Add test coverage and Storybook stories for the provider information components: the address block, the services list, the verified badge and the container that composes them, including one story per provider workflow state. @ericof [#24](https://github.com/collective/collective.casestudy/issues/24)
- Add test coverage for the content views, the metadata blocks and their registration, the add-on configuration, and the `useMetadataContent` hook; add Storybook stories for the views and the block edit forms. @ericof 
- Cover `ContactInfo`, `IndustryInfo`, `OrganizationHeader`, `OrganizationInfo` and the case studies slot with tests and stories, and split the configuration tests into one file per module under `config`. @ericof 



### Project


#### Breaking

- Convert the repository to a monorepo, with the Plone add-on now living in `backend`, a new Volto add-on in `frontend` and the documentation in `docs`. @ericof [#13](https://github.com/collective/collective.casestudy/issues/13)


#### Internal

- Regenerate the repository from the cookieplone `monorepo_addon` template, adding `repository.toml`, `docker-compose.yml`, a top level `Makefile` and dedicated GitHub Actions workflows for backend, frontend and documentation. @ericof [#13](https://github.com/collective/collective.casestudy/issues/13)
- Added @fosten to `.github/CODEOWNERS`. @ericof 
- Grant `contents: write` to the Storybook deploy job, so it can push to the `gh-pages` branch. @ericof 
- Skip the changelog check on pull requests labelled `skip changelog`, and have Dependabot apply that label to the pull requests it opens. @ericof 


#### Documentation

- Add a Sphinx / MyST documentation project under `docs`, with Vale styles and a Diátaxis based structure. @ericof [#13](https://github.com/collective/collective.casestudy/issues/13)



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
