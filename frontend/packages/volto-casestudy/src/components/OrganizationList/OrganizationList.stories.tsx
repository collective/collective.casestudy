import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationList from './OrganizationList';
import type { OrganizationSummary } from '../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  description: '',
  review_state: 'published',
  image_field: '',
  image_scales: null,
} as unknown as OrganizationSummary;

const GLOBEX = {
  ...ACME,
  '@id': 'https://6.demo.plone.org/en/organizations/globex',
  UID: 'globex-uid',
  title: 'Globex',
} as unknown as OrganizationSummary;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/OrganizationList',
  component: OrganizationList,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    items: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof OrganizationList>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { items: [ACME, GLOBEX] },
};

export const Single: Story = {
  args: { items: [ACME] },
};
