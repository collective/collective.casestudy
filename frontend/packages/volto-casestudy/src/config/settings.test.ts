import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import installSettings, { CONTENT_ICONS, CONTROLPANEL_ID } from './settings';

/** A registry stub holding just what `installSettings` touches. */
function makeConfig() {
  return {
    settings: {
      controlPanelsIcons: { dexterity_types: 'typesSVG' },
      contentIcons: { Document: 'pageSVG' },
    },
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

  it.each(['CaseStudy', 'Organization'])('gives %s a content icon', (type) => {
    const config = installSettings(makeConfig());
    expect(config.settings.contentIcons[type]).toBe(
      CONTENT_ICONS[type as keyof typeof CONTENT_ICONS],
    );
    expect(config.settings.contentIcons[type]).toBeTruthy();
  });

  it('keeps the content icons Volto already registered', () => {
    const config = installSettings(makeConfig());
    expect(config.settings.contentIcons.Document).toBe('pageSVG');
  });
});
