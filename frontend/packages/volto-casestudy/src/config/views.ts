import type { ConfigType } from '@plone/registry';
import type { ViewsConfig } from '@plone/types';

import CaseStudyView from '../components/Views/CaseStudyView/CaseStudyView';
import OrganizationView from '../components/Views/OrganizationView/OrganizationView';
import ProviderView from '../components/Views/ProviderView/ProviderView';

/**
 * Register the views of the add-on's content types.
 *
 * `CaseStudy` and `Organization` get content type views. `providerView` is a
 * layout view: the backend reports it as the layout of a provider whose
 * listing is public, and Volto resolves a layout view before a content type
 * view, so such an organization is rendered by `ProviderView`.
 *
 * @param config - The Volto configuration registry.
 * @returns The same registry, with the views registered.
 */
export default function install(config: ConfigType) {
  // `config.views` is typed as `Record<string, never> | ViewsConfig`, so
  // spreading it yields an object TypeScript cannot prove is a full
  // `ViewsConfig`. Volto always populates it before add-ons run.
  config.views = {
    ...config.views,
    contentTypesViews: {
      ...config.views?.contentTypesViews,
      CaseStudy: CaseStudyView,
      Organization: OrganizationView,
    },
    layoutViews: {
      ...config.views?.layoutViews,
      providerView: ProviderView,
    },
  } as ViewsConfig;

  return config;
}
