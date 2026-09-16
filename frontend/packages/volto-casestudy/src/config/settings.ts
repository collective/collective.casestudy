import type { ConfigType } from '@plone/registry';
import briefcaseSVG from '@plone/volto/icons/briefcase.svg';

/**
 * Configlet id from the backend's `controlpanel.xml`, which is also the last
 * segment of the panel's route (`/controlpanel/case_study`) and the key
 * Volto looks its icon up under.
 */
export const CONTROLPANEL_ID = 'case_study';

/**
 * Colours for the workflow states and transitions this add-on installs.
 *
 * Volto paints the state dot as an *inline* style read from
 * `config.settings.workflowMapping`, so these cannot come from a stylesheet.
 * Two helpers consume the map and key off different things: the current state
 * keys on the state id, the dropdown options key on the transition id, so both
 * sets are listed. Anything missing falls back to black.
 *
 * `pending` is deliberately absent — Volto already colours it, and these keys
 * are global across every workflow in the site.
 */
export const WORKFLOW_MAPPING = {
  // States, read by `getCurrentStateMapping` off `state.id`.
  created: { value: 'created', color: '#826a6a' },
  listed: { value: 'listed', color: '#007bc1' },
  verified: { value: 'verified', color: '#07461c' },
  archived: { value: 'archived', color: '#767676' },
  // Transitions, read by `getWorkflowOptions` off the last segment of the
  // transition URL. `value` names the state the transition leads to.
  review: { value: 'pending', color: '#f6a808' },
  list: { value: 'listed', color: '#007bc1' },
  verify: { value: 'verified', color: '#07461c' },
  unverify: { value: 'listed', color: '#007bc1' },
  archive: { value: 'archived', color: '#767676' },
};

export default function install(config: ConfigType) {
  // Without an entry Volto draws its generic placeholder, and this add-on's
  // panel reads as the one thing in the listing that did not finish
  // installing. A briefcase, matching the `string:briefcase` the classic UI
  // resolves from the same profile, so both interfaces show the same icon.
  config.settings.controlPanelsIcons = {
    ...config.settings.controlPanelsIcons,
    [CONTROLPANEL_ID]: briefcaseSVG,
  };

  // Both workflows of the chain render through Volto's own mapping helpers —
  // the additional `provider_workflow` selector included, since
  // volto-multiworkflow's shadowed Workflow component delegates to them.
  config.settings.workflowMapping = {
    ...config.settings.workflowMapping,
    ...WORKFLOW_MAPPING,
  };

  return config;
}
