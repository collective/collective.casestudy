import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import { CaseStudyMetadataView } from './View';
import type {
  CaseStudy,
  OrganizationSummary,
  PreviewImageLink,
} from '../../../types/content';

const PREVIEW_IMAGE = {
  '@id': 'https://6.demo.plone.org/en/welcome-to-plone-6',
  '@type': 'Image',
  UID: 'preview-uid',
  description: '',
  image_field: 'image',
  review_state: 'published',
  title: 'Screenshot',
  image_scales: {
    image: [
      {
        'content-type': 'image/png',
        download: '@@images/image.png',
        filename: 'shot.png',
        width: 1200,
        height: 800,
        size: 12345,
        scales: {
          preview: {
            download: '@@images/image-400.png',
            width: 400,
            height: 267,
          },
        },
      },
    ],
  },
} as unknown as PreviewImageLink;

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
} as unknown as CaseStudy;

const BLOCK_DATA = { '@type': 'case_study_metadata' };

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 720, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Blocks/CaseStudyMetadata',
  component: CaseStudyMetadataView,
  decorators: [withWrapper],
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    data: { control: 'object' },
    properties: { control: 'object' },
  },
} satisfies Meta<typeof CaseStudyMetadataView>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { data: BLOCK_DATA, properties: baseContent },
};

export const WithScreenshot: Story = {
  args: {
    data: BLOCK_DATA,
    properties: {
      ...baseContent,
      preview_image_link: PREVIEW_IMAGE,
      preview_caption_link: 'The new Plone.org home page',
    },
  },
};

export const MultipleUsagesAndVersions: Story = {
  args: {
    data: BLOCK_DATA,
    properties: {
      ...baseContent,
      usages: [
        { token: 'portal', title: 'Portal' },
        { token: 'intranet', title: 'Intranet' },
        { token: 'kb', title: 'Knowledge Base' },
      ],
      versions: [
        { token: '6.1', title: 'Plone 6.1' },
        { token: '6.0', title: 'Plone 6.0' },
      ],
    },
  },
};

export const WithoutWebsite: Story = {
  args: {
    data: BLOCK_DATA,
    properties: { ...baseContent, remoteUrl: '' },
  },
};

export const WithoutSubjects: Story = {
  args: {
    data: BLOCK_DATA,
    properties: { ...baseContent, subjects: [] },
  },
};

export const Minimal: Story = {
  args: {
    data: BLOCK_DATA,
    properties: {
      ...baseContent,
      industry: null,
      usages: [],
      versions: [],
      remoteUrl: '',
      subjects: [],
    },
  },
};

export const WithOrganizationsAndProviders: Story = {
  args: {
    data: BLOCK_DATA,
    properties: {
      ...baseContent,
      organizations: [ACME],
      providers: [AGENCY],
    },
  },
};

export const NoContent: Story = {
  args: { data: BLOCK_DATA, properties: undefined },
};
