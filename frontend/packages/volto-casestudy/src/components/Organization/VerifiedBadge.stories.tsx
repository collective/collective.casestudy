import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import VerifiedBadge from './VerifiedBadge';

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/VerifiedBadge',
  component: VerifiedBadge,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    className: { control: 'text' },
  },
} satisfies Meta<typeof VerifiedBadge>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

/** The badge takes its colours from CSS custom properties on `:root`. */
export const Recoloured: Story = {
  args: {},
  decorators: [
    (Story) => (
      <div
        style={
          {
            '--verified-badge-fill': '#e6f4ea',
            '--verified-badge-stroke': '#07461c',
          } as React.CSSProperties
        }
      >
        <Story />
      </div>
    ),
  ],
};
