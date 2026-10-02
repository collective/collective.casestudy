import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import InfoBox from './InfoBox';

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24, width: 320 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/InfoBlocks/InfoBox',
  component: InfoBox,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    name: { control: 'text' },
    title: { control: 'text' },
    as: { control: 'select', options: ['p', 'ul', 'div'] },
    className: { control: 'text' },
  },
} satisfies Meta<typeof InfoBox>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { name: 'usage', title: 'Usage', children: 'Portal, Intranet' },
};

export const AsList: Story = {
  args: {
    name: 'services',
    title: 'Services',
    as: 'ul',
    children: (
      <>
        <li>Design</li>
        <li>Development</li>
      </>
    ),
  },
};
