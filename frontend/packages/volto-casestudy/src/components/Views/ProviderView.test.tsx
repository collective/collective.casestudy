import { describe, it, expect, beforeAll, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import config from '@plone/volto/registry';
import applySocialMedia from '@plonegovbr/volto-social-media';
import ProviderView from './ProviderView';
import type { CaseStudySummary, Organization } from '../../types/content';

vi.mock('react-intl', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-intl')>();
  return {
    ...actual,
    useIntl: () => ({
      formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
        defaultMessage,
    }),
  };
});

/**
 * A listed provider, as the backend serializes it for the `providerView`
 * layout. The children are rendered for real: the view is only the page
 * around them.
 */
const LISTED = {
  '@id': 'http://localhost:8080/Plone/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  description: 'A Plone solution provider',
  layout: 'providerView',
  preview_image_link: null,
  preview_caption_link: null,
  organization_size: null,
  social_links: [],
  subjects: [],
  is_provider: true,
  address: 'Avenida Paulista 1636',
  address_2: null,
  city: 'Sao Paulo',
  state: 'SP',
  postal_code: '01310-200',
  country: { token: 'BR', title: 'Brazil' },
  services: [
    { token: 'dev', title: 'Development' },
    { token: 'hosting', title: 'Hosting' },
  ],
  case_studies: { provided: [], received: [] },
  workflow_states: {
    simple_publication_workflow: 'published',
    provider_workflow: 'listed',
  },
} as unknown as Organization;

const CASE_STUDY = {
  '@id': 'http://localhost:8080/Plone/plone-org',
  '@type': 'CaseStudy',
  UID: 'plone-org-uid',
  title: 'New Plone.org',
  description: 'A rebuild of the community site',
  review_state: 'listed',
  image_field: '',
  image_scales: null,
} as unknown as CaseStudySummary;

function renderView(content: Partial<Organization> = {}) {
  return render(
    <Wrapper anonymous>
      <ProviderView content={{ ...LISTED, ...content } as Organization} />
    </Wrapper>,
  );
}

describe('ProviderView', () => {
  beforeAll(() => {
    // `SocialNetworkIcon` resolves each network through a `socialNetwork`
    // utility; the add-on registering them is not loaded by the test config.
    applySocialMedia(config);
  });

  it('renders the title as the first heading', () => {
    const { container } = renderView();
    expect(
      container.querySelector('h1.documentFirstHeading')?.textContent,
    ).toBe('Acme Inc.');
  });

  it('renders the description', () => {
    const { container } = renderView();
    expect(container.querySelector('p.description')?.textContent).toBe(
      'A Plone solution provider',
    );
  });

  it('marks the wrapper as the provider view', () => {
    const { container } = renderView();
    const wrapper = container.querySelector('#page-document');
    expect(wrapper?.className).toContain('provider-view');
  });

  it('renders the provider information', () => {
    const { container, getByText } = renderView();
    expect(container.querySelector('.provider-info')).not.toBeNull();
    expect(getByText('Avenida Paulista 1636')).toBeTruthy();
    expect(container.querySelectorAll('li.service-item')).toHaveLength(2);
  });

  it('shows no verified badge for a listed provider', () => {
    const { container } = renderView();
    expect(container.querySelector('.verified-badge')).toBeNull();
  });

  it('shows the verified badge for a verified provider', () => {
    const { container } = renderView({
      workflow_states: {
        simple_publication_workflow: 'published',
        provider_workflow: 'verified',
      },
    });
    expect(container.querySelector('.verified-badge')).not.toBeNull();
  });

  it('renders no logo when the relation is empty', () => {
    const { container } = renderView();
    expect(container.querySelector('.organizationLogo')).toBeNull();
  });

  it('renders the social networks container', () => {
    const { container } = renderView();
    expect(container.querySelector('.socialNetworks')).not.toBeNull();
  });

  it('renders no case studies block when there are none', () => {
    const { container } = renderView();
    expect(container.querySelector('.caseStudies')).toBeNull();
  });

  it('renders the case studies the provider delivered', () => {
    const { container, getByText } = renderView({
      case_studies: { provided: [CASE_STUDY], received: [] },
    });
    expect(container.querySelector('.caseStudies')).not.toBeNull();
    expect(getByText('New Plone.org')).toBeTruthy();
  });
});
