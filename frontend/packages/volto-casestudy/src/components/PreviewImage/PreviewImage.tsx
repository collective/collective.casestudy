import React from 'react';
import { getPreviewImageSource } from '@plone-collective/volto-casestudy/helpers/preview';
import type { PreviewImageLink } from '@plone-collective/volto-casestudy/types/content';
import './preview-image.scss';

export interface PreviewImageProps {
  link: PreviewImageLink | null;
  caption: string | null;
  /** Image scale to prefer; see `getPreviewImageSource`. */
  scale?: string;
}

/** The image a `preview_image_link` relation points to, or nothing. */
export const PreviewImage = ({ link, caption, scale }: PreviewImageProps) => {
  const source = getPreviewImageSource(link, scale);
  if (!source) return null;

  return (
    <img
      src={source.src}
      alt={caption || ''}
      height={source.height}
      width={source.width}
      className="preview-image"
    />
  );
};

export default PreviewImage;
