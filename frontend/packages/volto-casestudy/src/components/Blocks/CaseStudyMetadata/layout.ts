/**
 * `full` spans the container, image first and the rest as boxes below;
 * `compact` is a narrow aside floated to the right of the text.
 */
export type CaseStudyMetadataLayout = 'full' | 'compact';

export const DEFAULT_LAYOUT: CaseStudyMetadataLayout = 'full';

/** Image scale requested for each layout. */
export const LAYOUT_IMAGE_SCALE: Record<CaseStudyMetadataLayout, string> = {
  full: 'great',
  compact: 'preview',
};

/**
 * Resolve the stored layout, falling back to {@link DEFAULT_LAYOUT} for
 * blocks saved before the option existed or holding an unknown value.
 *
 * @param value - The block's `layout` field.
 * @returns A known layout.
 */
export function resolveLayout(value: unknown): CaseStudyMetadataLayout {
  return value === 'full' || value === 'compact' ? value : DEFAULT_LAYOUT;
}
