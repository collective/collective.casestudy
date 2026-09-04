import { describe, it, expect } from 'vitest';
import {
  getPreviewImageSource,
  getSummaryImageField,
  hasSummaryImage,
  SUMMARY_IMAGE_FIELD,
} from './preview';
import type { ContentSummary, PreviewImageLink } from '../types/content';

/**
 * Shaped after a real plone.restapi payload: `image_scales` maps the field
 * name to a list, and `download` is relative to the item's `@id`.
 */
function makeLink(scales: Record<string, any> = {}): PreviewImageLink {
  return {
    '@id': 'http://localhost:8080/plone/shot',
    '@type': 'Image',
    UID: 'uid-1',
    description: '',
    image_field: 'image',
    review_state: 'published',
    title: 'Screenshot',
    image_scales: {
      image: [
        {
          'content-type': 'image/png',
          download: '@@images/image-1-abc.png',
          filename: 'shot.png',
          width: 1200,
          height: 800,
          size: 67,
          scales,
        } as any,
      ],
    },
  } as PreviewImageLink;
}

describe('getPreviewImageSource', () => {
  it('joins the item @id with the scale download path', () => {
    const link = makeLink({
      preview: {
        download: '@@images/image-preview.png',
        width: 400,
        height: 300,
      },
    });
    expect(getPreviewImageSource(link)).toEqual({
      src: 'http://localhost:8080/plone/shot/@@images/image-preview.png',
      width: 400,
      height: 300,
    });
  });

  it('falls back to the full-size download when the scale is missing', () => {
    expect(getPreviewImageSource(makeLink())).toEqual({
      src: 'http://localhost:8080/plone/shot/@@images/image-1-abc.png',
      width: 1200,
      height: 800,
    });
  });

  it('honours a requested scale name', () => {
    const link = makeLink({
      teaser: {
        download: '@@images/image-teaser.png',
        width: 600,
        height: 400,
      },
    });
    expect(getPreviewImageSource(link, 'teaser')?.src).toBe(
      'http://localhost:8080/plone/shot/@@images/image-teaser.png',
    );
  });

  it('returns undefined when there is no relation', () => {
    expect(getPreviewImageSource(null)).toBeUndefined();
    expect(getPreviewImageSource(undefined)).toBeUndefined();
  });

  it('returns undefined when image_scales is null', () => {
    const link = { ...makeLink(), image_scales: null } as PreviewImageLink;
    expect(getPreviewImageSource(link)).toBeUndefined();
  });

  it('returns undefined when the image list is empty', () => {
    const link = {
      ...makeLink(),
      image_scales: { image: [] },
    } as PreviewImageLink;
    expect(getPreviewImageSource(link)).toBeUndefined();
  });
});

/** A relation summary, as it arrives inside a relation field. */
function makeSummary(overrides: Partial<ContentSummary> = {}): ContentSummary {
  return {
    '@id': 'http://localhost:8080/plone/acme',
    '@type': 'Organization',
    UID: 'acme-uid',
    description: '',
    review_state: 'published',
    title: 'Acme Inc.',
    image_field: 'preview_image_link',
    image_scales: {
      preview_image_link: [
        {
          'content-type': 'image/png',
          download: '@@images/image-200.png',
          filename: 'acme.png',
          width: 200,
          height: 80,
          scales: {},
        },
      ],
    },
    ...overrides,
  } as unknown as ContentSummary;
}

describe('getSummaryImageField', () => {
  it('uses the field the catalog reported', () => {
    expect(getSummaryImageField(makeSummary())).toBe('preview_image_link');
  });

  it('falls back to the relation field, never to `image`', () => {
    // Volto's `Image` guesses `image`, which no content type here uses.
    expect(getSummaryImageField(makeSummary({ image_field: '' }))).toBe(
      SUMMARY_IMAGE_FIELD,
    );
  });

  it('honours a content type that really does have an image field', () => {
    expect(getSummaryImageField(makeSummary({ image_field: 'image' }))).toBe(
      'image',
    );
  });
});

describe('hasSummaryImage', () => {
  it('is true when the reported field carries a scale', () => {
    expect(hasSummaryImage(makeSummary())).toBe(true);
  });

  it('is false when the relation is broken', () => {
    expect(hasSummaryImage(makeSummary({ image_scales: null }))).toBe(false);
  });

  it('is false when the field is present but empty', () => {
    expect(
      hasSummaryImage(
        makeSummary({ image_scales: { preview_image_link: [] } }),
      ),
    ).toBe(false);
  });

  it('is false when the scales are under a different field', () => {
    expect(
      hasSummaryImage(
        makeSummary({
          image_field: 'image',
          image_scales: { preview_image_link: [{} as never] },
        }),
      ),
    ).toBe(false);
  });

  it('resolves through the fallback when image_field is empty', () => {
    expect(hasSummaryImage(makeSummary({ image_field: '' }))).toBe(true);
  });
});
