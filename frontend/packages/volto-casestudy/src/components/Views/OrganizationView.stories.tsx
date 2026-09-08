import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationView from './OrganizationView';
import type { Organization, PreviewImageLink } from '../../types/content';

const LOGO = {
  '@id': 'https://6.demo.plone.org/en/logos/acme',
  '@type': 'Image',
  UID: 'logo-uid',
  description: '',
  image_field: 'image',
  review_state: 'published',
  title: 'Acme logo',
  image_scales: {
    image: [
      {
        'content-type': 'image/png',
        download: '@@images/image.png',
        filename: 'acme.png',
        width: 600,
        height: 240,
        size: 12345,
        scales: {},
      },
    ],
  },
} as unknown as PreviewImageLink;

const baseContent = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  description: 'A company that has been running Plone since 2005.',
  preview_image_link: null,
  preview_caption_link: null,
  organization_size: { token: 'large', title: 'More than 30 employees' },
  social_links: [],
  subjects: [],
} as unknown as Organization;

const SOCIAL_LINKS = [
  {
    '@id': 'link-website',
    id: 'website',
    title: 'Web site',
    href: [{ '@id': 'https://acme.example', title: 'Acme' }],
  },
  {
    '@id': 'link-mastodon',
    id: 'mastodon',
    title: 'Mastodon',
    href: [{ '@id': 'https://plone.social/@acme', title: 'Acme' }],
  },
];

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 900, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Views/OrganizationView',
  component: OrganizationView,
  decorators: [withWrapper],
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
  argTypes: { content: { control: 'object' } },
} satisfies Meta<typeof OrganizationView>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { content: baseContent },
};

export const WithLogo: Story = {
  args: {
    content: {
      ...baseContent,
      preview_image_link: LOGO,
      preview_caption_link: 'The Acme logo',
    },
  },
};

export const WithSocialLinks: Story = {
  args: {
    content: { ...baseContent, social_links: SOCIAL_LINKS } as Organization,
  },
};

export const Complete: Story = {
  args: {
    content: {
      ...baseContent,
      preview_image_link: LOGO,
      preview_caption_link: 'The Acme logo',
      social_links: SOCIAL_LINKS,
    } as Organization,
  },
};

/** Provider fields the view only renders when `is_provider` is set. */
const PROVIDER_FIELDS = {
  is_provider: true,
  address: 'Avenida Paulista 1636',
  address_2: 'Sala 1504',
  city: 'São Paulo',
  state: 'SP',
  postal_code: '01310-200',
  country: { token: 'BR', title: 'Brazil' },
  services: [
    { token: 'design', title: 'Design' },
    { token: 'dev', title: 'Development' },
    { token: 'hosting', title: 'Hosting' },
  ],
};

export const Provider: Story = {
  args: {
    content: {
      ...baseContent,
      ...PROVIDER_FIELDS,
      workflow_states: { provider_workflow: 'listed' },
    } as unknown as Organization,
  },
};

/** The verified badge is the only difference from `Provider`. */
export const VerifiedProvider: Story = {
  args: {
    content: {
      ...baseContent,
      ...PROVIDER_FIELDS,
      workflow_states: { provider_workflow: 'verified' },
    } as unknown as Organization,
  },
};

/** `is_provider` false hides the whole provider block, fields or not. */
export const NotAProvider: Story = {
  args: {
    content: {
      ...baseContent,
      ...PROVIDER_FIELDS,
      is_provider: false,
      workflow_states: {},
    } as unknown as Organization,
  },
};
