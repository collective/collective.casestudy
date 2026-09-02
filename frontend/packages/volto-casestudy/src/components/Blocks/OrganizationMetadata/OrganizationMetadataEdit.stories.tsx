import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import OrganizationMetadataEdit from './Edit';

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 720, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Editor/Blocks/OrganizationMetadata',
  component: OrganizationMetadataEdit,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    data: { control: 'object' },
    selected: { control: 'boolean' },
  },
} satisfies Meta<typeof OrganizationMetadataEdit>;

export default meta;
type Story = StoryObj<typeof meta>;

// `selected` stays false: the settings form renders through `SidebarPortal`,
// which needs the editor's sidebar node -- there is none in Storybook.
export const CurrentPage: Story = {
  args: {
    data: { '@type': 'organization_metadata' },
    block: 'block-1',
    selected: false,
    onChangeBlock: () => {},
  },
};

export const CustomSource: Story = {
  args: {
    data: {
      '@type': 'organization_metadata',
      organization_source: [
        {
          '@id': 'https://6.demo.plone.org/en/another-organization',
          title: 'Another Organization',
        },
      ],
    },
    block: 'block-1',
    selected: false,
    onChangeBlock: () => {},
  },
};
