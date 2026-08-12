import type { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installBlocks from './config/blocks';
import installViews from './config/views';

function applyConfig(config: ConfigType) {
  installSettings(config);
  installBlocks(config);
  installViews(config);

  return config;
}

export default applyConfig;
