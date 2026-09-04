import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import CaseStudies from './CaseStudies';
import type { CaseStudySummary } from '../../types/content';

function caseStudy(
  id: string,
  title: string,
  description: string,
  withShot = true,
): CaseStudySummary {
  return {
    '@id': `https://6.demo.plone.org/en/${id}`,
    '@type': 'CaseStudy',
    UID: `${id}-uid`,
    title,
    description,
    review_state: 'published',
    image_field: withShot ? 'preview_image_link' : '',
    image_scales: withShot
      ? {
          preview_image_link: [
            {
              'content-type': 'image/png',
              download: '@@images/image.png',
              filename: `${id}.png`,
              width: 800,
              height: 600,
              base_path: `/en/screenshots/${id}`,
              scales: {},
            },
          ],
        }
      : null,
  } as unknown as CaseStudySummary;
}

const PROVIDED = [
  caseStudy(
    'plone-org',
    'New Plone.org',
    'A rebuild of the community site on Plone 6, with a Volto front end.',
  ),
  caseStudy(
    'news-site',
    'News Site',
    'A high-traffic newsroom running Plone behind a CDN.',
  ),
];

const RECEIVED = [
  caseStudy(
    'intranet',
    'Corporate Intranet',
    'An intranet for 3,000 employees, replacing a legacy portal.',
  ),
];

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 900, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/CaseStudies',
  component: CaseStudies,
  decorators: [withWrapper],
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
  argTypes: { case_studies: { control: 'object' } },
} satisfies Meta<typeof CaseStudies>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BothGroups: Story = {
  args: { case_studies: { provided: PROVIDED, received: RECEIVED } },
};

export const OnlyProvided: Story = {
  args: { case_studies: { provided: PROVIDED, received: [] } },
};

export const OnlyReceived: Story = {
  args: { case_studies: { provided: [], received: RECEIVED } },
};

export const WithoutScreenshots: Story = {
  args: {
    case_studies: {
      provided: [],
      received: [
        caseStudy(
          'intranet',
          'Corporate Intranet',
          'No screenshot yet.',
          false,
        ),
      ],
    },
  },
};

export const Empty: Story = {
  args: { case_studies: { provided: [], received: [] } },
};
