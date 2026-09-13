import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationSocialLinks from './OrganizationSocialLinks';
import type { Organization } from '../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  social_links: [
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
  ],
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/OrganizationSocialLinks',
  component: OrganizationSocialLinks,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof OrganizationSocialLinks>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithLinks: Story = {
  args: { content: ACME },
};

/** With no links the container is still there, and empty. */
export const WithoutLinks: Story = {
  args: {
    content: { ...ACME, social_links: [] } as unknown as Organization,
  },
};
