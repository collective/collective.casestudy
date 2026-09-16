import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import IndustryInfo from './IndustryInfo';
import type { Organization } from '../../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  industry: { token: 'finance', title: 'Financial Services' },
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/IndustryInfo',
  component: IndustryInfo,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof IndustryInfo>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { content: ACME },
};

/** The token rides along as a class, so a site can style per industry. */
export const NonProfit: Story = {
  args: {
    content: {
      ...ACME,
      industry: { token: 'non-profit', title: 'Non-profit' },
    } as unknown as Organization,
  },
};

/** With no industry set the block drops out entirely, heading included. */
export const Empty: Story = {
  args: {
    content: { ...ACME, industry: null } as unknown as Organization,
  },
};
