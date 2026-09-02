import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import { OrganizationMetadataView } from './View';
import type {
  Organization,
  PreviewImageLink,
  SocialMediaItem,
} from '../../../types/content';

const PREVIEW_IMAGE = {
  '@id': 'https://6.demo.plone.org/en/company-1',
  '@type': 'Image',
  UID: 'preview-uid',
  description: '',
  image_field: 'image',
  review_state: 'published',
  title: 'Office',
  image_scales: {
    image: [
      {
        'content-type': 'image/png',
        download: '@@images/image.png',
        filename: 'office.png',
        width: 1200,
        height: 800,
        size: 12345,
        scales: {
          preview: {
            download: '@@images/image-400.png',
            width: 400,
            height: 267,
          },
        },
      },
    ],
  },
} as unknown as PreviewImageLink;

const WEBSITE: SocialMediaItem = {
  '@id': 'urn:website',
  id: 'website',
  title: 'Company site',
  href: [{ '@id': 'https://company1.com', title: 'Company site' }],
};

const MASTODON: SocialMediaItem = {
  '@id': 'urn:mastodon',
  id: 'mastodon',
  title: 'Mastodon',
  href: [{ '@id': 'https://plone.social/@company1', title: 'Mastodon' }],
};

const baseContent = {
  '@id': 'https://6.demo.plone.org/en/company-1',
  '@type': 'Organization',
  title: 'Company 1',
  description: 'A Plone Company provider',
  preview_image_link: null,
  preview_caption_link: null,
  organization_size: { token: 'large', title: 'More than 30 employees' },
  social_links: [WEBSITE, MASTODON],
  contact_name: 'John Doe',
  contact_email: 'doe@company1.com',
  contact_phone: '+4917632259823',
  address: null,
  address_2: null,
  city: null,
  state: null,
  postal_code: null,
  country: { token: 'DE', title: 'Germany' },
  is_provider: true,
  services: [
    { token: 'design', title: 'Design / Theming' },
    { token: 'dev', title: 'Development / Integration' },
  ],
  subjects: ['Plone', 'Intranet'],
} as unknown as Organization;

const BLOCK_DATA = { '@type': 'organization_metadata' };

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 720, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Blocks/OrganizationMetadata',
  component: OrganizationMetadataView,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    data: { control: 'object' },
    properties: { control: 'object' },
  },
} satisfies Meta<typeof OrganizationMetadataView>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { data: BLOCK_DATA, properties: baseContent },
};

export const WithScreenshot: Story = {
  args: {
    data: BLOCK_DATA,
    properties: {
      ...baseContent,
      preview_image_link: PREVIEW_IMAGE,
      preview_caption_link: 'The company office',
    },
  },
};

export const WithoutWebsite: Story = {
  args: {
    data: BLOCK_DATA,
    properties: { ...baseContent, social_links: [MASTODON] },
  },
};

export const NoSocialLinks: Story = {
  args: {
    data: BLOCK_DATA,
    properties: { ...baseContent, social_links: [] },
  },
};

export const PlainOrganization: Story = {
  args: {
    data: BLOCK_DATA,
    properties: {
      ...baseContent,
      is_provider: false,
      services: [],
      social_links: [WEBSITE],
    },
  },
};

export const Minimal: Story = {
  args: {
    data: BLOCK_DATA,
    properties: {
      ...baseContent,
      contact_name: null,
      contact_email: null,
      contact_phone: null,
      country: null,
      organization_size: null,
      social_links: [],
      subjects: [],
    },
  },
};

export const NoContent: Story = {
  args: { data: BLOCK_DATA, properties: undefined },
};
