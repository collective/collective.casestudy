import { describe, it, expect, beforeAll } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import config from '@plone/volto/registry';
import applySocialMedia from '@plonegovbr/volto-social-media';
import OrganizationHeader from './OrganizationHeader';
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

const ACME = {
  '@id': 'http://localhost:8080/Plone/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  description: 'A company using Plone',
  preview_image_link: null,
  preview_caption_link: null,
  social_links: [],
  subjects: [],
} as unknown as Organization;

function renderHeader(
  content: Partial<Organization> = {},
  { label = '', isVerified = false } = {},
) {
  return render(
    <Wrapper anonymous>
      <OrganizationHeader
        content={{ ...ACME, ...content } as Organization}
        label={label}
        isVerified={isVerified}
      />
    </Wrapper>,
  );
}

describe('OrganizationHeader', () => {
  beforeAll(() => {
    // `SocialNetworkIcon` resolves each network through a `socialNetwork`
    // utility; the add-on registering them is not loaded by the test config.
    applySocialMedia(config);
  });

  it('renders the title as the first heading', () => {
    const { container } = renderHeader();
    expect(
      container.querySelector('h1.organizationTitle')?.textContent,
    ).toContain('Acme Inc.');
  });

  it('renders the description', () => {
    const { container } = renderHeader();
    expect(
      container.querySelector('p.organizationDescription')?.textContent,
    ).toBe('A company using Plone');
  });

  it('renders the label it is given', () => {
    const { container } = renderHeader({}, { label: 'Provider' });
    expect(container.querySelector('.organizationLabel')?.textContent).toBe(
      'Provider',
    );
  });

  it('renders no logo when the relation is empty', () => {
    const { container } = renderHeader({ preview_image_link: null });
    expect(container.querySelector('.organizationLogo')).toBeNull();
  });

  it('renders the logo from preview_image_link', () => {
    const { container } = renderHeader({ preview_image_link: LOGO });
    const img = container.querySelector('.organizationLogo img');
    expect(img?.getAttribute('src')).toBe('/logos/acme/@@images/image-300.png');
  });

  it('renders a social networks container even with no links', () => {
    const { container } = renderHeader({ social_links: [] });
    expect(container.querySelector('.socialNetworks')).toBeTruthy();
  });

  it('survives content with no social_links key at all', () => {
    const { container } = renderHeader({
      social_links: undefined as unknown as [],
    });
    expect(container.querySelector('h1.organizationTitle')).toBeTruthy();
  });
});

describe('OrganizationHeader verified badge', () => {
  beforeAll(() => {
    applySocialMedia(config);
  });

  it('is shown when the caller says the organization is verified', () => {
    const { container } = renderHeader({}, { isVerified: true });
    expect(container.querySelector('.verified-badge')).not.toBeNull();
  });

  it('is hidden otherwise', () => {
    // The header reads a boolean; deciding it is the view's job.
    const { container } = renderHeader({}, { isVerified: false });
    expect(container.querySelector('.verified-badge')).toBeNull();
  });

  it('sits inside the title, next to the name', () => {
    const { container } = renderHeader({}, { isVerified: true });
    expect(
      container.querySelector('h1.organizationTitle .verified-badge'),
    ).not.toBeNull();
  });
});
