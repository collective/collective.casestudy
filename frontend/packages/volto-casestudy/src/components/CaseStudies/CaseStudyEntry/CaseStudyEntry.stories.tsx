import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import CaseStudyEntry from './CaseStudyEntry';
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

/** The entry is an `<li>`, so a story has to supply the list around it. */
const withList: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 320, padding: 24 }}>
      <ul style={{ padding: 0, margin: 0, listStyle: 'none' }}>
        <Story />
      </ul>
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Organization/CaseStudyEntry',
  component: CaseStudyEntry,
  decorators: [withList],
  tags: ['autodocs'],
  argTypes: { item: { control: 'object' } },
} satisfies Meta<typeof CaseStudyEntry>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    item: caseStudy(
      'plone-org',
      'New Plone.org',
      'A rebuild of the community site on Plone 6, with a Volto front end.',
    ),
  },
};

export const WithoutScreenshot: Story = {
  args: {
    item: caseStudy(
      'intranet',
      'Corporate Intranet',
      'No screenshot yet.',
      false,
    ),
  },
};

export const WithoutDescription: Story = {
  args: { item: caseStudy('news-site', 'News Site', '') },
};

export const LongDescription: Story = {
  args: {
    item: caseStudy(
      'news-site',
      'News Site',
      'A high-traffic newsroom running Plone behind a CDN, serving several ' +
        'million page views a month across a dozen editorial teams, each with ' +
        'its own workflow and publication calendar.',
    ),
  },
};
