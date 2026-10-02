import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import PreviewImage from './PreviewImage';
import type { PreviewImageLink } from '../../types/content';

const LINK = {
  '@id': 'http://localhost:8080/plone/shot',
  image_scales: {
    image: [
      {
        download: '@@images/image-1-abc.png',
        width: 1200,
        height: 800,
        scales: {
          preview: {
            download: '@@images/image-preview.png',
            width: 400,
            height: 300,
          },
        },
      },
    ],
  },
} as unknown as PreviewImageLink;

describe('PreviewImage', () => {
  it('renders the preview scale by default', () => {
    const { container } = render(
      <PreviewImage link={LINK} caption="A screenshot" />,
    );
    const img = container.querySelector('img.preview-image');
    expect(img?.getAttribute('src')).toBe(
      'http://localhost:8080/plone/shot/@@images/image-preview.png',
    );
    expect(img?.getAttribute('width')).toBe('400');
    expect(img?.getAttribute('alt')).toBe('A screenshot');
  });

  it('falls back to the original when the scale is missing', () => {
    const { container } = render(
      <PreviewImage link={LINK} caption={null} scale="great" />,
    );
    const img = container.querySelector('img.preview-image');
    expect(img?.getAttribute('src')).toBe(
      'http://localhost:8080/plone/shot/@@images/image-1-abc.png',
    );
    expect(img?.getAttribute('alt')).toBe('');
  });

  it('renders nothing without a link', () => {
    const { container } = render(<PreviewImage link={null} caption={null} />);
    expect(container.firstChild).toBeNull();
  });
});
