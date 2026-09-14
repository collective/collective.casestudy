import React from 'react';
import type { Decorator, Meta, StoryObj } from '@storybook/react';
import Wrapper from '@plone/volto/storybook';

import ProviderView from './ProviderView';
import type {
  CaseStudySummary,
  Organization,
  PreviewImageLink,
} from '../../types/content';

const LOGO = {
  '@id': 'https://6.demo.plone.org/en/logos/acme',
  '@type': 'Image',
  UID: 'logo-uid',
  description: '',
  image_field: 'image',
  review_state: 'published',
  title: 'Acme logo',
  image_scales: {
    image: [
      {
        'content-type': 'image/png',
        download: '@@images/image.png',
        filename: 'acme.png',
        width: 600,
        height: 240,
        size: 12345,
        scales: {},
      },
    ],
  },
} as unknown as PreviewImageLink;

const SOCIAL_LINKS = [
  {
    '@id': 'link-website',
    id: 'website',
    title: 'Web site',
    href: [{ '@id': 'https://acme.example', title: 'Acme' }],
  },
  {
    '@id': 'link-mastodon',
    id: 'mastodon',
    title: 'Mastodon',
    href: [{ '@id': 'https://plone.social/@acme', title: 'Acme' }],
  },
];

/** Build a case study summary, as the serializer nests it under `case_studies`. */
function caseStudy(
  id: string,
  title: string,
  description: string,
): CaseStudySummary {
  return {
    '@id': `https://6.demo.plone.org/en/${id}`,
    '@type': 'CaseStudy',
    UID: `${id}-uid`,
    title,
    description,
    review_state: 'listed',
    image_field: '',
    image_scales: null,
  } as unknown as CaseStudySummary;
}

const CASE_STUDIES = {
  provided: [
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
  ],
  received: [
    caseStudy(
      'intranet',
      'Corporate Intranet',
      'The intranet Acme runs for its own 300 employees.',
    ),
  ],
};

/**
 * A listed provider, as the backend serializes it: `layout` is `providerView`
 * and `provider_workflow` is `listed`.
 */
const baseContent = {
  '@id': 'https://6.demo.plone.org/en/organizations/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  description: 'A Plone solution provider since 2005.',
  layout: 'providerView',
  preview_image_link: null,
  preview_caption_link: null,
  organization_size: { token: 'large', title: 'More than 30 employees' },
  social_links: [],
  subjects: [],
  is_provider: true,
  address: 'Avenida Paulista 1636',
  address_2: 'Sala 1504',
  city: 'São Paulo',
  state: 'SP',
  postal_code: '01310-200',
  country: { token: 'BR', title: 'Brazil' },
  services: [
    { token: 'design', title: 'Design' },
    { token: 'dev', title: 'Development' },
    { token: 'hosting', title: 'Hosting' },
  ],
  case_studies: { provided: [], received: [] },
  workflow_states: [
    'simple_publication_workflow|published',
    'provider_workflow|listed',
  ],
} as unknown as Organization;

/** The same provider, verified. */
const verified = {
  ...baseContent,
  workflow_states: [
    'simple_publication_workflow|published',
    'provider_workflow|verified',
  ],
} as unknown as Organization;

const withWrapper: Decorator = (Story) => (
  <Wrapper anonymous>
    <div style={{ width: 900, padding: 24 }}>
      <Story />
    </div>
  </Wrapper>
);

const meta = {
  title: 'Public/Views/ProviderView',
  component: ProviderView,
  decorators: [withWrapper],
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
  argTypes: { content: { control: 'object' } },
} satisfies Meta<typeof ProviderView>;

export default meta;
type Story = StoryObj<typeof meta>;

/** A listed provider: address and services, no verified badge. */
export const Listed: Story = {
  args: { content: baseContent },
};

/** The verified badge is the only difference from `Listed`. */
export const Verified: Story = {
  args: { content: verified },
};

export const WithLogo: Story = {
  args: {
    content: {
      ...baseContent,
      preview_image_link: LOGO,
      preview_caption_link: 'The Acme logo',
    } as Organization,
  },
};

export const WithSocialLinks: Story = {
  args: {
    content: { ...baseContent, social_links: SOCIAL_LINKS } as Organization,
  },
};

/** Projects the provider delivered, and case studies about the provider itself. */
export const WithCaseStudies: Story = {
  args: {
    content: { ...baseContent, case_studies: CASE_STUDIES } as Organization,
  },
};

/** With no services the services block is dropped, and the address stands alone. */
export const WithoutServices: Story = {
  args: {
    content: { ...baseContent, services: [] } as unknown as Organization,
  },
};

/** Everything at once, on a verified provider. */
export const Complete: Story = {
  args: {
    content: {
      ...verified,
      preview_image_link: LOGO,
      preview_caption_link: 'The Acme logo',
      social_links: SOCIAL_LINKS,
      case_studies: CASE_STUDIES,
    } as Organization,
  },
};
