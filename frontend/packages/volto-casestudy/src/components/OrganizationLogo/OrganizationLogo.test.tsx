import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import OrganizationLogo from './OrganizationLogo';
import type { Organization, PreviewImageLink } from '../../types/content';

const LOGO = {
  '@id': 'http://localhost:8080/Plone/logos/acme',
  '@type': 'Image',
  UID: 'logo-uid',
  title: 'Acme logo',
  description: '',
  review_state: 'published',
  image_field: 'image',
  image_scales: {
    image: [
      {
        'content-type': 'image/png',
        download: '@@images/image-300.png',
        filename: 'acme.png',
        width: 300,
        height: 120,
        scales: {},
      },
    ],
  },
} as unknown as PreviewImageLink;

const WITH_LOGO = {
  '@id': 'http://localhost:8080/Plone/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  preview_image_link: LOGO,
  preview_caption_link: 'The Acme logo',
} as unknown as Organization;

function renderLogo(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <OrganizationLogo content={content} className={className} />
    </Wrapper>,
  );
}

describe('OrganizationLogo', () => {
  it('renders nothing when the relation is empty', () => {
    const none = {
      ...WITH_LOGO,
      preview_image_link: null,
    } as unknown as Organization;
    const { container } = renderLogo(none);
    expect(container.querySelector('.organizationLogo')).toBeNull();
  });

  it('survives content with no logo field at all', () => {
    const bare = { '@id': '/acme' } as unknown as Organization;
    const { container } = renderLogo(bare);
    expect(container.querySelector('.organizationLogo')).toBeNull();
  });

  it('renders the image from preview_image_link', () => {
    const { container } = renderLogo(WITH_LOGO);
    const img = container.querySelector('.organizationLogo img');
    expect(img?.getAttribute('src')).toBe('/logos/acme/@@images/image-300.png');
  });

  it('uses the caption field as the text alternative', () => {
    const { container } = renderLogo(WITH_LOGO);
    expect(
      container.querySelector('.organizationLogo img')?.getAttribute('alt'),
    ).toBe('The Acme logo');
  });

  it('falls back to the image title when there is no caption', () => {
    const uncaptioned = {
      ...WITH_LOGO,
      preview_caption_link: null,
    } as unknown as Organization;
    const { container } = renderLogo(uncaptioned);
    expect(
      container.querySelector('.organizationLogo img')?.getAttribute('alt'),
    ).toBe('Acme logo');
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderLogo(WITH_LOGO, 'providerLogo');
    const el = container.querySelector('.organizationLogo');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('providerLogo')).toBe(true);
  });
});
