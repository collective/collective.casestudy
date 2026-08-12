import type { ConfigType } from '@plone/registry';
import CaseStudyBlockInfo from '../components/Blocks/CaseStudyMetadata';
import ProviderBlockInfo from '../components/Blocks/ProviderMetadata';

export default function installBlocks(config: ConfigType) {
  config.blocks.blocksConfig.case_study_metadata = CaseStudyBlockInfo;
  config.blocks.blocksConfig.provider_metadata = ProviderBlockInfo;

  config.blocks.initialBlocks = {
    ...config.blocks.initialBlocks,
    CaseStudy: ['title', 'case_study_metadata'],
    Provider: ['title', 'provider_metadata'],
  };

  return config;
}
