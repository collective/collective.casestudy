import type { ConfigType } from '@plone/registry';
import CaseStudyBlockInfo from '../components/Blocks/CaseStudyMetadata';
import OrganizationBlockInfo from '../components/Blocks/OrganizationMetadata';

export default function installBlocks(config: ConfigType) {
  config.blocks.blocksConfig.case_study_metadata = CaseStudyBlockInfo;
  config.blocks.blocksConfig.organization_metadata = OrganizationBlockInfo;

  config.blocks.initialBlocks = {
    ...config.blocks.initialBlocks,
    CaseStudy: ['title', 'description', 'case_study_metadata'],
  };

  return config;
}
