import type { Image } from '@plone/types';
import type {
  ContentSummary,
  PreviewImageLink,
} from '@plone-collective/volto-casestudy/types/content';

/** Scale requested for the metadata block screenshot. */
export const PREVIEW_SCALE = 'preview';

export interface PreviewImageSource {
  src: string;
  width?: number;
  height?: number;
}

/**
 * Build a renderable source from a `preview_image_link` relation.
 *
 * plone.restapi emits `image_scales` as `{ <field>: [ … ] }` and every
 * `download` path inside it is relative to the *linked image's* `@id`, so the
 * two have to be joined back together.
 *
 * Falls back to the full-size download when the requested scale has not been
 * generated.
 *
 * @param link - The `preview_image_link` value, possibly null.
 * @param scaleName - Scale to prefer.
 * @returns The source, or `undefined` when there is no usable image.
 */
export function getPreviewImageSource(
  link: PreviewImageLink | null | undefined,
  scaleName: string = PREVIEW_SCALE,
): PreviewImageSource | undefined {
  const image: Image | undefined = link?.image_scales?.image?.[0];
  if (!image || !link) return undefined;

  const scale = image.scales?.[scaleName];
  const download = scale?.download ?? image.download;
  if (!download) return undefined;

  return {
    src: `${link['@id']}/${download}`,
    width: scale?.width ?? image.width,
    height: scale?.height ?? image.height,
  };
}

/**
 * Field `plone.volto` indexes for content whose image is a relation rather
 * than an image field of its own — every content type in this add-on.
 */
export const SUMMARY_IMAGE_FIELD = 'preview_image_link';

/**
 * Name of the `image_scales` entry holding a summary's image.
 *
 * `@plone/volto`'s `Image` falls back to the field `image` when a summary
 * carries no `image_field`, which is never the right guess here — so the
 * field is resolved once and handed to it explicitly.
 *
 * @param item - The content summary.
 * @returns The field name to read `image_scales` under.
 */
export function getSummaryImageField(item: ContentSummary): string {
  return item.image_field || SUMMARY_IMAGE_FIELD;
}

/**
 * Does this summary carry an image that can be rendered?
 *
 * A summary with no image at all has an empty `image_field`, and a broken
 * relation leaves `image_scales` null — neither is renderable.
 *
 * @param item - The content summary.
 */
export function hasSummaryImage(item: ContentSummary): boolean {
  return Boolean(item.image_scales?.[getSummaryImageField(item)]?.length);
}
