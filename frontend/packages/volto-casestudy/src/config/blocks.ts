import type { ConfigType } from '@plone/registry';

import { CaseStudyMetadataView, CaseStudyMetadataEdit } from '../components';

import icon from '@plone/volto/icons/list-bullet.svg';

export default function installBlocks(config: ConfigType) {
  config.blocks.blocksConfig.case_study_metadata = {
    id: 'case_study_metadata',
    title: 'Case Study Metadata',
    view: CaseStudyMetadataView,
    edit: CaseStudyMetadataEdit,
    icon: icon,
    group: 'text',
    restricted: ({ contentType }) => {
      return contentType !== 'CaseStudy';
    },
  };

  config.blocks.initialBlocks = {
    ...config.blocks.initialBlocks,
    CaseStudy: ['title', 'case_study_metadata'],
  };

  return config;
}
