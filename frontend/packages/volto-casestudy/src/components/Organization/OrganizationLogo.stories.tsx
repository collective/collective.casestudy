import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationLogo from './OrganizationLogo';
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

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  preview_image_link: LOGO,
  preview_caption_link: 'The Acme logo',
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 600, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/OrganizationLogo',
  component: OrganizationLogo,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof OrganizationLogo>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithCaption: Story = {
  args: { content: ACME },
};

/** With no caption, the image title becomes the text alternative. */
export const WithoutCaption: Story = {
  args: {
    content: { ...ACME, preview_caption_link: null } as Organization,
  },
};

/** An organization with no logo renders nothing at all. */
export const WithoutLogo: Story = {
  args: {
    content: { ...ACME, preview_image_link: null } as Organization,
  },
};
