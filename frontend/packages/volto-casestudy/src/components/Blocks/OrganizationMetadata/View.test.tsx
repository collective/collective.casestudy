import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { OrganizationMetadataView } from './View';
import type { Organization } from '../../../types/content';

vi.mock('react-intl', () => ({
  defineMessages: (messages: Record<string, unknown>) => messages,
  useIntl: () => ({
    formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
      defaultMessage,
  }),
}));

const BLOCK_DATA = { '@type': 'organization_metadata' };

const baseContent = {
  '@id': 'http://localhost:8080/plone/company-1',
  '@type': 'Organization',
  title: 'Company 1',
  description: '',
  preview_image_link: null,
  preview_caption_link: null,
  organization_size: null,
  social_links: [],
  contact_name: null,
  contact_email: null,
  contact_phone: null,
  address: null,
  address_2: null,
  city: null,
  state: null,
  postal_code: null,
  country: null,
  is_provider: false,
  services: [],
  subjects: [],
} as unknown as Organization;

function renderView(content: Partial<Organization>) {
  return render(
    <OrganizationMetadataView
      data={BLOCK_DATA}
      properties={{ ...baseContent, ...content } as Organization}
    />,
  );
}

describe('OrganizationMetadataView', () => {
  it('renders nothing when there is no content', () => {
    const { container } = render(
      <OrganizationMetadataView data={BLOCK_DATA} properties={undefined} />,
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders the contact fields', () => {
    const { container } = renderView({
      contact_name: 'John Doe',
      contact_email: 'doe@company1.com',
      contact_phone: '+4917632259823',
    });
    expect(container.textContent).toContain('John Doe');
    expect(container.textContent).toContain('doe@company1.com');
    expect(container.textContent).toContain('+4917632259823');
  });

  it('renders country and organization size titles', () => {
    const { container } = renderView({
      country: { token: 'DE', title: 'Germany' },
      organization_size: { token: 'large', title: 'More than 30 employees' },
    });
    expect(container.textContent).toContain('Germany');
    expect(container.textContent).toContain('More than 30 employees');
  });

  it('renders the website from the social_links website entry', () => {
    const { container } = renderView({
      social_links: [
        {
          '@id': 'urn:1',
          id: 'website',
          title: 'Company site',
          href: [{ '@id': 'https://company1.com', title: 'Company site' }],
        },
      ],
    });
    const link = container.querySelector('a');
    expect(link?.getAttribute('href')).toBe('https://company1.com');
    expect(link?.getAttribute('rel')).toBe('noopener noreferrer');
  });

  it('omits the website section when social_links has no website entry', () => {
    const { container } = renderView({
      social_links: [
        {
          '@id': 'urn:2',
          id: 'mastodon',
          title: 'Mastodon',
          href: [{ '@id': 'https://plone.social/@c1', title: 'Mastodon' }],
        },
      ],
    });
    expect(container.querySelector('a')).toBeNull();
  });

  it('omits the website section when social_links is empty', () => {
    const { container } = renderView({ social_links: [] });
    expect(container.querySelector('a')).toBeNull();
  });

  it('renders the preview image from preview_image_link', () => {
    const { container } = renderView({
      preview_caption_link: 'Office',
      preview_image_link: {
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
      } as any,
    });
    const img = container.querySelector('img.preview-image');
    expect(img?.getAttribute('src')).toBe(
      'http://localhost:8080/plone/shot/@@images/image-preview.png',
    );
    expect(img?.getAttribute('alt')).toBe('Office');
  });

  it('renders the subjects list without crashing', () => {
    // Regression: the old ProviderMetadata referenced `messages.what`, which
    // that module never defined, so this branch threw at runtime.
    const { container } = renderView({ subjects: ['Plone', 'Intranet'] });
    expect(container.textContent).toContain('Plone');
    expect(container.textContent).toContain('Intranet');
  });
});
