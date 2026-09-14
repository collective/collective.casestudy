import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import ProviderInfo from './ProviderInfo';
import type { Organization } from '../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
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
  workflow_states: [
    'simple_publication_workflow|published',
    'provider_workflow|verified',
  ],
} as unknown as Organization;

/** Build the same provider in another `provider_workflow` state. */
function inState(state: string): Organization {
  return {
    ...ACME,
    workflow_states: [
      'simple_publication_workflow|published',
      `provider_workflow|${state}`,
    ],
  } as unknown as Organization;
}

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/ProviderInfo',
  component: ProviderInfo,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof ProviderInfo>;

export default meta;
type Story = StoryObj<typeof meta>;

/** The badge appears only in `verified`. */
export const Verified: Story = {
  args: { content: ACME },
};

export const Listed: Story = {
  args: { content: inState('listed') },
};

export const Created: Story = {
  args: { content: inState('created') },
};

export const Archived: Story = {
  args: { content: inState('archived') },
};

/** With no services the block is dropped, and the address stands alone. */
export const WithoutServices: Story = {
  args: {
    content: { ...ACME, services: [] } as unknown as Organization,
  },
};

/**
 * An organization whose chain never gained `provider_workflow` — the badge
 * has no state to read and stays hidden.
 */
export const WithoutTheWorkflow: Story = {
  args: {
    content: {
      ...ACME,
      workflow_states: ['simple_publication_workflow|published'],
    } as unknown as Organization,
  },
};
