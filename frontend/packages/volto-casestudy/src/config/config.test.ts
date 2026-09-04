import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import installBlocks from './blocks';
import installViews from './views';
import installSettings from './settings';
import { CONTROLPANEL_ID } from './settings';
import installWidgets from './widgets';
import { TERMS_WIDGET } from './widgets';
import applyConfig from '../index';
import CaseStudyBlockInfo from '../components/Blocks/CaseStudyMetadata';
import OrganizationBlockInfo from '../components/Blocks/OrganizationMetadata';

/** A registry stub holding just what the install functions touch. */
function makeConfig() {
  return {
    blocks: {
      blocksConfig: { title: { id: 'title' } },
      initialBlocks: { Document: ['title', 'text'] },
    },
    views: {
      contentTypesViews: { Document: 'DocumentView' },
      layoutViews: { document_view: 'DocumentView' },
    },
    settings: { controlPanelsIcons: { dexterity_types: 'typesSVG' } },
    widgets: { widget: { text: 'TextWidget' } },
  } as unknown as ConfigType;
}

describe('installBlocks', () => {
  it('registers both metadata blocks', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.blocksConfig.case_study_metadata).toBe(
      CaseStudyBlockInfo,
    );
    expect(config.blocks.blocksConfig.organization_metadata).toBe(
      OrganizationBlockInfo,
    );
  });

  it('keeps the blocks Volto already registered', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.blocksConfig.title).toBeTruthy();
  });

  it('gives each content type its own metadata block by default', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.initialBlocks.CaseStudy).toEqual([
      'title',
      'case_study_metadata',
    ]);
    expect(config.blocks.initialBlocks.Organization).toEqual([
      'title',
      'organization_metadata',
    ]);
  });

  it('does not drop initial blocks configured elsewhere', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.initialBlocks.Document).toEqual(['title', 'text']);
  });
});

describe('installViews', () => {
  it('registers a view for each content type', () => {
    const config = installViews(makeConfig());
    expect(config.views.contentTypesViews.CaseStudy).toBeTruthy();
    expect(config.views.contentTypesViews.Organization).toBeTruthy();
  });

  it('keeps the views Volto already registered', () => {
    const config = installViews(makeConfig());
    expect(config.views.contentTypesViews.Document).toBe('DocumentView');
    expect(config.views.layoutViews.document_view).toBe('DocumentView');
  });

  it('survives a registry with no views at all', () => {
    const config = installViews({} as unknown as ConfigType);
    expect(config.views.contentTypesViews.CaseStudy).toBeTruthy();
  });
});

describe('installWidgets', () => {
  it('registers the widget the backend asks for by name', () => {
    const config = installWidgets(makeConfig());
    expect(config.widgets.widget[TERMS_WIDGET]).toBeTruthy();
  });

  it('keeps the widgets Volto already registered', () => {
    const config = installWidgets(makeConfig());
    expect(config.widgets.widget.text).toBeTruthy();
  });
});

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

describe('applyConfig', () => {
  it('runs every installer', () => {
    const config = applyConfig(makeConfig());
    expect(config.blocks.blocksConfig.case_study_metadata).toBeTruthy();
    expect(config.views.contentTypesViews.Organization).toBeTruthy();
    expect(config.widgets.widget[TERMS_WIDGET]).toBeTruthy();
    expect(config.settings.controlPanelsIcons[CONTROLPANEL_ID]).toBeTruthy();
  });

  it('returns the same config object', () => {
    const config = makeConfig();
    expect(applyConfig(config)).toBe(config);
  });
});
