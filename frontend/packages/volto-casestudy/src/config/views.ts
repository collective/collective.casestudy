import type { ConfigType } from '@plone/registry';

import { CaseStudyView } from '../components/';

export default function install(config: ConfigType) {
  config.views = {
    ...config.views,
    contentTypesViews: {
      ...config.views?.contentTypesViews,
      CaseStudy: CaseStudyView,
    },
  };

  return config;
}
