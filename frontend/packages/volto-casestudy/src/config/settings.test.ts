import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import installSettings, { CONTROLPANEL_ID } from './settings';

/** A registry stub holding just what `installSettings` touches. */
function makeConfig() {
  return {
    settings: { controlPanelsIcons: { dexterity_types: 'typesSVG' } },
  } as unknown as ConfigType;
}

describe('installSettings', () => {
  it('returns the config it was given', () => {
    const config = makeConfig();
    expect(installSettings(config)).toBe(config);
  });

  it('gives the control panel an icon', () => {
    const config = installSettings(makeConfig());
    expect(config.settings.controlPanelsIcons[CONTROLPANEL_ID]).toBeTruthy();
  });

  it('keys the icon by the configlet id the backend declares', () => {
    // `/controlpanel/case_study` -- the last segment is the key.
    expect(CONTROLPANEL_ID).toBe('case_study');
  });

  it('keeps the icons Volto already registered', () => {
    const config = installSettings(makeConfig());
    expect(config.settings.controlPanelsIcons.dexterity_types).toBe('typesSVG');
  });
});
