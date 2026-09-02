import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import CaseStudyMetadataEdit from './Edit';

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 720, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Editor/Blocks/CaseStudyMetadata',
  component: CaseStudyMetadataEdit,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    data: { control: 'object' },
    selected: { control: 'boolean' },
  },
} satisfies Meta<typeof CaseStudyMetadataEdit>;

export default meta;
type Story = StoryObj<typeof meta>;

// `selected` stays false: the settings form renders through `SidebarPortal`,
// which needs the editor's sidebar node -- there is none in Storybook.
export const CurrentPage: Story = {
  args: {
    data: { '@type': 'case_study_metadata' },
    block: 'block-1',
    selected: false,
    onChangeBlock: () => {},
  },
};

export const CustomSource: Story = {
  args: {
    data: {
      '@type': 'case_study_metadata',
      case_study_source: [
        {
          '@id': 'https://6.demo.plone.org/en/another-case-study',
          title: 'Another Case Study',
        },
      ],
    },
    block: 'block-1',
    selected: false,
    onChangeBlock: () => {},
  },
};
