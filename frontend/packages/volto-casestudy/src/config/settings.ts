import type { ConfigType } from '@plone/registry';
import briefcaseSVG from '@plone/volto/icons/briefcase.svg';

/**
 * Configlet id from the backend's `controlpanel.xml`, which is also the last
 * segment of the panel's route (`/controlpanel/case_study`) and the key
 * Volto looks its icon up under.
 */
export const CONTROLPANEL_ID = 'case_study';

export default function install(config: ConfigType) {
  // Without an entry Volto draws its generic placeholder, and this add-on's
  // panel reads as the one thing in the listing that did not finish
  // installing. A briefcase, matching the `string:briefcase` the classic UI
  // resolves from the same profile, so both interfaces show the same icon.
  config.settings.controlPanelsIcons = {
    ...config.settings.controlPanelsIcons,
    [CONTROLPANEL_ID]: briefcaseSVG,
  };

  return config;
}
