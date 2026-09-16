import type { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installBlocks from './config/blocks';
import installViews from './config/views';
import installWidgets from './config/widgets';
import installSlots from './config/slots';
import './theme/root.css';

function applyConfig(config: ConfigType) {
  installSettings(config);
  installBlocks(config);
  installViews(config);
  installWidgets(config);
  installSlots(config);

  return config;
}

export default applyConfig;
