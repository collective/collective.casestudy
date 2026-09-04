import type { ConfigType } from '@plone/registry';
import type { ViewsConfig } from '@plone/types';

import CaseStudyView from '../components/Views/CaseStudyView';
import OrganizationView from '../components/Views/OrganizationView';

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
  } as ViewsConfig;

  return config;
}
