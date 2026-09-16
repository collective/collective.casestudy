import { describe, it, expect, beforeAll } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import config from '@plone/volto/registry';
import applySocialMedia from '@plonegovbr/volto-social-media';
import OrganizationView from './OrganizationView';
import installSlots from '../../../config/slots';
import type { Organization, PreviewImageLink } from '../../../types/content';

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

const baseContent = {
  '@id': 'http://localhost:8080/Plone/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  description: 'A company using Plone',
  preview_image_link: null,
  preview_caption_link: null,
  organization_size: null,
  social_links: [],
  subjects: [],
} as unknown as Organization;

function renderView(content: Partial<Organization> = {}) {
  return render(
    <Wrapper anonymous>
      <OrganizationView
        content={{ ...baseContent, ...content } as Organization}
      />
    </Wrapper>,
  );
}

describe('OrganizationView', () => {
  beforeAll(() => {
    // `SocialNetworkIcon` resolves each network through a `socialNetwork`
    // utility; the add-on registering them is not loaded by the test config.
    applySocialMedia(config);
    // The case studies reach the page through a slot, which the add-on
    // registers at install time -- the test config never runs that.
    installSlots(config);
  });

  it('renders the title as the first heading', () => {
    const { container } = renderView();
    // The heading holds the title and a space before the badge slot, so the
    // text is not an exact match.
    expect(
      container.querySelector('h1.organizationTitle')?.textContent,
    ).toContain('Acme Inc.');
  });

  it('renders the description', () => {
    const { container } = renderView();
    expect(
      container.querySelector('p.organizationDescription')?.textContent,
    ).toBe('A company using Plone');
  });

  it('renders no logo when the relation is empty', () => {
    const { container } = renderView({ preview_image_link: null });
    expect(container.querySelector('.organizationLogo')).toBeNull();
  });

  it('renders the logo from preview_image_link', () => {
    const { container } = renderView({ preview_image_link: LOGO });
    const img = container.querySelector('.organizationLogo img');
    expect(img?.getAttribute('src')).toBe('/logos/acme/@@images/image-300.png');
  });

  it('captions the logo with the caption field', () => {
    const { container } = renderView({
      preview_image_link: LOGO,
      preview_caption_link: 'The Acme logo',
    });
    expect(
      container.querySelector('.organizationLogo img')?.getAttribute('alt'),
    ).toBe('The Acme logo');
  });

  it('falls back to the image title when there is no caption', () => {
    const { container } = renderView({
      preview_image_link: LOGO,
      preview_caption_link: null,
    });
    expect(
      container.querySelector('.organizationLogo img')?.getAttribute('alt'),
    ).toBe('Acme logo');
  });

  it('renders a social networks container even with no links', () => {
    const { container } = renderView({ social_links: [] });
    expect(container.querySelector('.socialNetworks')).toBeTruthy();
  });

  it('survives content with no social_links key at all', () => {
    const { container } = renderView({
      social_links: undefined as unknown as [],
    });
    expect(container.querySelector('h1.organizationTitle')).toBeTruthy();
  });

  it('renders one entry per social link', () => {
    const { container } = renderView({
      social_links: [
        {
          '@id': 'link-1',
          id: 'website',
          title: 'Web site',
          href: [{ '@id': 'https://acme.example', title: 'Acme' }],
        },
        {
          '@id': 'link-2',
          id: 'mastodon',
          title: 'Mastodon',
          href: [{ '@id': 'https://plone.social/@acme', title: 'Acme' }],
        },
      ],
    });
    expect(
      container.querySelectorAll('.social-networks > li.item'),
    ).toHaveLength(2);
  });

  it('skips a social link with no target', () => {
    const { container } = renderView({
      social_links: [
        { '@id': 'link-1', id: 'website', title: 'Web site', href: [] },
      ],
    });
    expect(
      container.querySelectorAll('.social-networks > li.item'),
    ).toHaveLength(0);
  });

  it('marks the wrapper as the organization view', () => {
    const { container } = renderView();
    const wrapper = container.querySelector('#page-document');
    expect(wrapper?.className).toContain('organization-view');
  });

  it('renders no provider information, even for a provider', () => {
    // A provider with a public listing is rendered by `ProviderView`.
    const { container } = renderView({
      is_provider: true,
      services: [{ token: 'dev', title: 'Development' }],
      workflow_states: [
        'simple_publication_workflow|published',
        'provider_workflow|verified',
      ],
    } as unknown as Partial<Organization>);
    expect(container.querySelector('.provider-info')).toBeNull();
    expect(container.querySelector('.verified-badge')).toBeNull();
  });
});
