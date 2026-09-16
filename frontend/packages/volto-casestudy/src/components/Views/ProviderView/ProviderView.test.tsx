import { describe, it, expect, beforeAll, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import config from '@plone/volto/registry';
import applySocialMedia from '@plonegovbr/volto-social-media';
import ProviderView from './ProviderView';
import installSlots from '../../../config/slots';
import type { CaseStudySummary, Organization } from '../../../types/content';

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
  workflow_states: [
    'simple_publication_workflow|published',
    'provider_workflow|listed',
  ],
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

/** A provider whose `provider_workflow` is in `state`, or out of the chain. */
function withState(state: string | null): Partial<Organization> {
  return {
    workflow_states: state
      ? ['simple_publication_workflow|published', `provider_workflow|${state}`]
      : ['simple_publication_workflow|published'],
  } as unknown as Partial<Organization>;
}

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
    // The case studies reach the page through a slot, which the add-on
    // registers at install time -- the test config never runs that.
    installSlots(config);
  });

  it('renders the title as the provider heading', () => {
    const { container } = renderView();
    expect(
      container.querySelector('h1.organizationTitle')?.textContent,
    ).toContain('Acme Inc.');
  });

  it('renders the description', () => {
    const { container } = renderView();
    expect(
      container.querySelector('p.organizationDescription')?.textContent,
    ).toBe('A Plone solution provider');
  });

  it('labels the page as a provider', () => {
    const { container } = renderView();
    expect(container.querySelector('.organizationLabel')?.textContent).toBe(
      'Provider',
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

  it('renders no logo when the relation is empty', () => {
    const { container } = renderView();
    expect(container.querySelector('.organizationLogo')).toBeNull();
  });

  it('renders the social networks container', () => {
    const { container } = renderView();
    expect(container.querySelector('.socialNetworks')).not.toBeNull();
  });
});

describe('ProviderView verified badge', () => {
  beforeAll(() => {
    applySocialMedia(config);
  });

  it('is shown when the provider workflow says verified', () => {
    const { container } = renderView(withState('verified'));
    expect(container.querySelector('.verified-badge')).not.toBeNull();
  });

  it.each(['created', 'pending', 'listed', 'archived'])(
    'is hidden in the %s state',
    (state) => {
      const { container } = renderView(withState(state));
      expect(container.querySelector('.verified-badge')).toBeNull();
    },
  );

  it('is hidden when the workflow is not in the chain', () => {
    const { container } = renderView(withState(null));
    expect(container.querySelector('.verified-badge')).toBeNull();
  });

  it('is hidden when workflow_states is missing entirely', () => {
    const { container } = renderView({
      workflow_states: undefined,
    } as unknown as Partial<Organization>);
    expect(container.querySelector('.verified-badge')).toBeNull();
  });

  it('reads verified from the provider workflow only', () => {
    /* A `verified` state of any other workflow must not verify. */
    const { container } = renderView({
      workflow_states: [
        'simple_publication_workflow|published',
        'another_workflow|verified',
      ],
    } as unknown as Partial<Organization>);
    expect(container.querySelector('.verified-badge')).toBeNull();
  });
});

describe('ProviderView about section', () => {
  beforeAll(() => {
    applySocialMedia(config);
  });

  it('is omitted when the provider has no text', () => {
    const { container } = renderView();
    expect(container.querySelector('.providerAboutSection')).toBeNull();
  });

  it('renders the rich text when it is set', () => {
    const { container, getByText } = renderView({
      text: {
        data: '<p>Acme has built Plone sites since 2005.</p>',
        'content-type': 'text/html',
        encoding: 'utf-8',
      },
    });
    expect(container.querySelector('.providerAboutSection')).not.toBeNull();
    expect(getByText('About')).toBeTruthy();
    expect(
      container.querySelector('.providerAboutSection .text')?.innerHTML,
    ).toContain('Acme has built Plone sites since 2005.');
  });
});

describe('ProviderView case studies', () => {
  beforeAll(() => {
    applySocialMedia(config);
    installSlots(config);
  });

  it('renders no case studies block when there are none', () => {
    const { container } = renderView();
    expect(container.querySelector('.case-studies')).toBeNull();
  });

  it('renders the case studies the provider delivered', () => {
    const { container, getByText } = renderView({
      case_studies: { provided: [CASE_STUDY], received: [] },
    });
    expect(container.querySelector('.case-studies')).not.toBeNull();
    expect(getByText('New Plone.org')).toBeTruthy();
  });
});
