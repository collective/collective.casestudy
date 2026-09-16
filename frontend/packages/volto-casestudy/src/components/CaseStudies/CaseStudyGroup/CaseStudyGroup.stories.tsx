import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import CaseStudyGroup from './CaseStudyGroup';
import type { CaseStudySummary } from '@plone-collective/volto-casestudy/types/content';

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

const ITEMS = [
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
  title: 'Public/Organization/CaseStudyGroup',
  component: CaseStudyGroup,
  decorators: [withWrapper],
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
  argTypes: { items: { control: 'object' }, title: { control: 'text' } },
} satisfies Meta<typeof CaseStudyGroup>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { items: ITEMS, title: 'Case studies' },
};

export const SingleEntry: Story = {
  args: { items: ITEMS.slice(0, 1), title: 'Projects' },
};

export const WithoutScreenshots: Story = {
  args: {
    items: [
      caseStudy('intranet', 'Corporate Intranet', 'No screenshot yet.', false),
    ],
    title: 'Case studies',
  },
};

/** An empty group renders nothing at all, heading included. */
export const Empty: Story = {
  args: { items: [], title: 'Case studies' },
};
