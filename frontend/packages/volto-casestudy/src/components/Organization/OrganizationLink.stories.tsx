import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationLink from './OrganizationLink';
import type { OrganizationSummary } from '../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  description: 'A company using Plone',
  review_state: 'published',
  image_field: '',
  image_scales: null,
} as unknown as OrganizationSummary;

const ACME_WITH_LOGO = {
  ...ACME,
  image_field: 'preview_image_link',
  image_scales: {
    preview_image_link: [
      {
        'content-type': 'image/png',
        download: '@@images/image-300.png',
        filename: 'acme.png',
        width: 300,
        height: 120,
        base_path: '/en/logos/acme',
        scales: {},
      },
    ],
  },
} as unknown as OrganizationSummary;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/OrganizationLink',
  component: OrganizationLink,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    item: { control: 'object' },
    showLogo: { control: 'boolean' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof OrganizationLink>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Title: Story = {
  args: { item: ACME },
};

export const Logo: Story = {
  args: { item: ACME_WITH_LOGO, showLogo: true },
};

export const LogoRequestedButMissing: Story = {
  args: { item: ACME, showLogo: true },
};
