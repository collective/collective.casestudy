# Changelog

<!-- You should *NOT* be adding new change log entries to this file.
     You should create a file in the news directory instead.
     For helpful instructions, please see:
     https://6.docs.plone.org/contributing/index.html#contributing-change-log-label
-->

<!-- towncrier release notes start -->

## 2.0.0-alpha.1 (2026-09-16)


### Breaking

- Require `@plone-collective/volto-multiworkflow` 1.0.0-alpha.2. `Organization['workflow_states']` is now the list of `<workflow-id>|<state-id>` values the backend serializes, and `ProviderInfo` reads the verified state from it with the add-on's `getWorkflowStates` and `formatWorkflowState` helpers. @ericof 


### Feature

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


### Internal

- Give every component a folder of its own, holding its implementation, styles, tests and stories. The information blocks — `AddressInfo`, `ContactInfo`, `IndustryInfo` and `ServicesInfo` — sit under `InfoBlocks`, `CaseStudyGroup` and `CaseStudyEntry` under `CaseStudies`, and each view under `Views/<Name>`. The repeated block rules moved into SCSS mixins shared by the callers, and the values they hardcoded into custom properties in `theme/root.css`. @ericof 
- Keep the monorepo-relative TypeScript paths in `tsconfig.json` and leave that file out of the published package. An IDE reads no other filename, so the paths have to live there; Volto's add-on registry reads a released add-on's `tsconfig.json` and lets its `paths` override the aliases it already resolved, so shipping them would break module resolution for consuming projects. @ericof 


### Tests

- Add test coverage and Storybook stories for the provider information components: the address block, the services list, the verified badge and the container that composes them, including one story per provider workflow state. @ericof [#24](https://github.com/collective/collective.casestudy/issues/24)
- Add test coverage for the content views, the metadata blocks and their registration, the add-on configuration, and the `useMetadataContent` hook; add Storybook stories for the views and the block edit forms. @ericof 
- Cover `ContactInfo`, `IndustryInfo`, `OrganizationHeader`, `OrganizationInfo` and the case studies slot with tests and stories, and split the configuration tests into one file per module under `config`. @ericof
