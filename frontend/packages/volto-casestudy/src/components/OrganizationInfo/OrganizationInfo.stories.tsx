import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationInfo from './OrganizationInfo';
import type { Organization } from '../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  address: 'Avenida Paulista 1636',
  address_2: 'Sala 1504',
  city: 'São Paulo',
  state: 'SP',
  postal_code: '01310-200',
  country: { token: 'BR', title: 'Brazil' },
  industry: { token: 'finance', title: 'Financial Services' },
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 900, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/OrganizationInfo',
  component: OrganizationInfo,
  decorators: [withWrapper],
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof OrganizationInfo>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Full: Story = {
  args: { content: ACME },
};

/** A block with nothing to show drops out; the rest keeps its layout. */
export const WithoutIndustry: Story = {
  args: {
    content: { ...ACME, industry: null } as unknown as Organization,
  },
};

export const WithoutAddress: Story = {
  args: {
    content: {
      ...ACME,
      address: null,
      address_2: null,
      city: null,
      state: null,
      postal_code: null,
      country: null,
    } as unknown as Organization,
  },
};

/** Nothing set at all: the blocks are empty and the section collapses. */
export const Empty: Story = {
  args: {
    content: {
      '@id': ACME['@id'],
      '@type': 'Organization',
      title: 'Acme Inc.',
    } as unknown as Organization,
  },
};
