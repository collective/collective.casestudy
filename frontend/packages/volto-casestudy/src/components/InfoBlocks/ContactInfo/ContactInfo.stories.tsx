import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import ContactInfo from './ContactInfo';
import type { Organization } from '../../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  contact_name: 'Ada Lovelace',
  contact_email: 'ada@acme.example',
  contact_phone: '+55 11 5555-0100',
} as unknown as Organization;

/** Every contact field left empty, which is how an organization starts. */
const EMPTY = {
  ...ACME,
  contact_name: null,
  contact_email: null,
  contact_phone: null,
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/ContactInfo',
  component: ContactInfo,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof ContactInfo>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Full: Story = {
  args: { content: ACME },
};

/** Only the fields that are set are rendered — no blank lines. */
export const EmailOnly: Story = {
  args: {
    content: {
      ...EMPTY,
      contact_email: 'ada@acme.example',
    } as unknown as Organization,
  },
};

export const WithoutPhone: Story = {
  args: {
    content: { ...ACME, contact_phone: null } as unknown as Organization,
  },
};

/** With nothing to show the block drops out entirely, heading included. */
export const Empty: Story = {
  args: { content: EMPTY },
};
