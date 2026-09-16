import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import applyConfig from './index';
import { CONTROLPANEL_ID } from './config/settings';
import { TERMS_WIDGET } from './config/widgets';

/** One `registerSlotComponent` call, as the stub below records it. */
interface RecordedSlot {
  slot: string;
  name: string;
  component: unknown;
  predicates?: ((args: unknown) => boolean)[];
}

/**
 * A registry stub holding what every installer touches.
 *
 * `applyConfig` runs all of them, so this one cannot be trimmed the way the
 * per-installer stubs in `config/*.test.ts` are.
 */
function makeConfig() {
  const registeredSlots: RecordedSlot[] = [];
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
    slots: {},
    registeredSlots,
    registerSlotComponent: (options: RecordedSlot) => {
      registeredSlots.push(options);
    },
  } as unknown as ConfigType;
}

/** The slot registrations a stub config recorded. */
function slotsOf(config: ConfigType): RecordedSlot[] {
  return (config as unknown as { registeredSlots: RecordedSlot[] })
    .registeredSlots;
}

describe('applyConfig', () => {
  it('runs every installer', () => {
    const config = applyConfig(makeConfig());
    expect(config.blocks.blocksConfig.case_study_metadata).toBeTruthy();
    expect(config.views.contentTypesViews.Organization).toBeTruthy();
    expect(config.widgets.widget[TERMS_WIDGET]).toBeTruthy();
    expect(config.settings.controlPanelsIcons[CONTROLPANEL_ID]).toBeTruthy();
    expect(slotsOf(config)).toHaveLength(1);
  });

  it('returns the same config object', () => {
    const config = makeConfig();
    expect(applyConfig(config)).toBe(config);
  });
});
