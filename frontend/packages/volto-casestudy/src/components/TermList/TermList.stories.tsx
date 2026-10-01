import type { Meta, StoryObj } from '@storybook/react';

import TermList from './TermList';

const meta = {
  title: 'Public/TermList',
  component: TermList,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    terms: { control: 'object' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof TermList>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    terms: [
      { token: 'portal', title: 'Portal' },
      { token: 'intranet', title: 'Intranet' },
      { token: 'kb', title: 'Knowledge Base' },
    ],
  },
};

export const SingleTerm: Story = {
  args: { terms: [{ token: '6.0', title: 'Plone 6.0' }] },
};
