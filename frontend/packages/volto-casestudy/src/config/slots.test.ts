import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import installSlots, {
  ORGANIZATION_FOOTER_SLOT,
  hasCaseStudies,
} from './slots';
import CaseStudiesSlot from '../components/CaseStudies/CaseStudiesSlot';

/** One `registerSlotComponent` call, as the stub below records it. */
interface RecordedSlot {
  slot: string;
  name: string;
  component: unknown;
  predicates?: ((args: unknown) => boolean)[];
}

/** A registry stub holding just what `installSlots` touches. */
function makeConfig() {
  const registeredSlots: RecordedSlot[] = [];
  return {
    slots: {},
    // The real registry stores these; recording them is enough to assert
    // what the add-on asked for.
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

describe('installSlots', () => {
  it('registers a component into the case studies slot', () => {
    const config = installSlots(makeConfig());
    const [entry] = slotsOf(config);
    expect(entry.slot).toBe(ORGANIZATION_FOOTER_SLOT);
    expect(entry.component).toBe(CaseStudiesSlot);
  });

  it('guards it with the hasCaseStudies predicate', () => {
    // Without the predicate the band would render on every organization,
    // empty heading and all.
    const config = installSlots(makeConfig());
    expect(slotsOf(config)[0].predicates).toEqual([hasCaseStudies]);
  });

  it('returns the config it was given', () => {
    const config = makeConfig();
    expect(installSlots(config)).toBe(config);
  });
});

describe('hasCaseStudies', () => {
  /** The predicate is called with what `SlotRenderer` collects. */
  function args(provided: unknown[], received: unknown[]) {
    return {
      content: { case_studies: { provided, received } },
    } as unknown as Parameters<typeof hasCaseStudies>[0];
  }

  it('is true when the organization delivered one', () => {
    expect(hasCaseStudies(args([{}], []))).toBe(true);
  });

  it('is true when the organization is the subject of one', () => {
    expect(hasCaseStudies(args([], [{}]))).toBe(true);
  });

  it('is false when both relations are empty', () => {
    expect(hasCaseStudies(args([], []))).toBe(false);
  });

  it('is false when the key is missing entirely', () => {
    expect(hasCaseStudies({ content: {} as unknown as never })).toBe(false);
  });

  it('is false when there is no content at all', () => {
    // An `Add` route renders slots before there is any content to read.
    expect(hasCaseStudies({})).toBe(false);
  });
});
