import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationHeader from './OrganizationHeader';
import type { Organization, PreviewImageLink } from '../../types/content';

const LOGO = {
  '@id': 'https://6.demo.plone.org/en/logos/acme',
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
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  description: 'A company using Plone since 2005.',
  preview_image_link: null,
  preview_caption_link: null,
  social_links: [
    {
      '@id': 'link-1',
      id: 'website',
      title: 'Web site',
      href: [{ '@id': 'https://acme.example', title: 'Acme' }],
    },
  ],
  subjects: [],
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 900, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/OrganizationHeader',
  component: OrganizationHeader,
  decorators: [withWrapper],
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    label: { control: 'text' },
    isVerified: { control: 'boolean' },
  },
} satisfies Meta<typeof OrganizationHeader>;

export default meta;
type Story = StoryObj<typeof meta>;

/** How `OrganizationView` renders it: no label, never verified. */
export const Plain: Story = {
  args: { content: ACME, label: '', isVerified: false },
};

/** How `ProviderView` renders a listed provider. */
export const Provider: Story = {
  args: { content: ACME, label: 'Provider', isVerified: false },
};

/** A verified provider: the badge sits next to the name. */
export const VerifiedProvider: Story = {
  args: { content: ACME, label: 'Provider', isVerified: true },
};

export const WithLogo: Story = {
  args: {
    content: { ...ACME, preview_image_link: LOGO } as unknown as Organization,
    label: 'Provider',
    isVerified: true,
  },
};

export const WithoutSocialLinks: Story = {
  args: {
    content: { ...ACME, social_links: [] } as unknown as Organization,
    label: '',
    isVerified: false,
  },
};
