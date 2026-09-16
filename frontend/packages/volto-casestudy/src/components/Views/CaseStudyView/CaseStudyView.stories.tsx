import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import CaseStudyView from './CaseStudyView';
import type { CaseStudy, OrganizationSummary } from '../../../types/content';

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

const AGENCY = {
  ...ACME,
  '@id': 'https://6.demo.plone.org/en/organizations/an-agency',
  UID: 'agency-uid',
  title: 'An Agency',
} as unknown as OrganizationSummary;

/** Blocks a freshly created Case Study starts with, per `config/blocks`. */
const blocks = {
  'block-title': { '@type': 'title' },
  'block-description': { '@type': 'description' },
  'block-metadata': { '@type': 'case_study_metadata' },
};

const baseContent = {
  '@id': 'https://6.demo.plone.org/en/plone-org',
  '@type': 'CaseStudy',
  title: 'New Plone.org',
  description: 'An explanation about the new Plone.org',
  remoteUrl: 'https://plone.org',
  preview_image_link: null,
  preview_caption_link: null,
  industry: { token: 'ngo', title: 'Non-government organization (NGO)' },
  usages: [{ token: 'portal', title: 'Portal' }],
  versions: [{ token: '6.0', title: 'Plone 6.0' }],
  organizations: [],
  providers: [],
  subjects: ['Tag 1', 'Tag 2'],
  blocks,
  blocks_layout: {
    items: ['block-title', 'block-description', 'block-metadata'],
  },
} as unknown as CaseStudy;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 900, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Views/CaseStudyView',
  component: CaseStudyView,
  decorators: [withWrapper],
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
  argTypes: { content: { control: 'object' } },
} satisfies Meta<typeof CaseStudyView>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { content: baseContent, location: { pathname: '/en/plone-org' } },
};

export const WithOrganizationsAndProviders: Story = {
  args: {
    content: {
      ...baseContent,
      organizations: [ACME],
      providers: [AGENCY],
    } as CaseStudy,
    location: { pathname: '/en/plone-org' },
  },
};

export const WithoutBlocks: Story = {
  args: {
    content: {
      ...baseContent,
      blocks: {},
      blocks_layout: { items: [] },
    } as unknown as CaseStudy,
    location: { pathname: '/en/plone-org' },
  },
};
