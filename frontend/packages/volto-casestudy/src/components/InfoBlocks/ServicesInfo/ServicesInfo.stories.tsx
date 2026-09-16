import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import ServicesInfo from './ServicesInfo';
import type { Organization } from '../../../types/content';

const ACME = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  services: [
    { token: 'design', title: 'Design' },
    { token: 'dev', title: 'Development' },
    { token: 'hosting', title: 'Hosting' },
    { token: 'training', title: 'Training' },
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
  title: 'Public/Organization/ServicesInfo',
  component: ServicesInfo,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    content: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof ServicesInfo>;

export default meta;
type Story = StoryObj<typeof meta>;

export const EveryService: Story = {
  args: { content: ACME },
};

export const SingleService: Story = {
  args: {
    content: {
      ...ACME,
      services: [{ token: 'hosting', title: 'Hosting' }],
    } as unknown as Organization,
  },
};

/**
 * `ProviderInfo` hides the block entirely in this case — the story exists to
 * show what the component alone does with it.
 */
export const NoServices: Story = {
  args: {
    content: { ...ACME, services: [] } as unknown as Organization,
  },
};
