import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import AddressInfo from './AddressInfo';
import type { Organization } from '../../../types/content';

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
} as unknown as Organization;

/** Every address field left empty, which is how an organization starts. */
const EMPTY = {
  ...ACME,
  address: null,
  address_2: null,
  city: null,
  state: null,
  postal_code: null,
  country: null,
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/AddressInfo',
  component: AddressInfo,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof AddressInfo>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Full: Story = {
  args: { content: ACME },
};

/** Only the fields that are set are rendered — no blank lines. */
export const CityOnly: Story = {
  args: {
    content: { ...EMPTY, city: 'Berlin' } as unknown as Organization,
  },
};

/** The heading stays even when there is nothing to put under it. */
export const Empty: Story = {
  args: { content: EMPTY },
};

export const WithoutCountry: Story = {
  args: {
    content: { ...ACME, country: null } as unknown as Organization,
  },
};
