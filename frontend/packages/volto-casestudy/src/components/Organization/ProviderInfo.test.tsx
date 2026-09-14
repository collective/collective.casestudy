import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import ProviderInfo from './ProviderInfo';
import type { Organization } from '../../types/content';

/**
 * The children are rendered for real rather than mocked. A mock would assert
 * the props this component passes, never that `AddressInfo` and
 * `ServicesList` can render them.
 */
const VERIFIED = {
  '@id': 'http://localhost:8080/Plone/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
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
  workflow_states: [
    'simple_publication_workflow|published',
    'provider_workflow|verified',
  ],
} as unknown as Organization;

function withState(state: string | null): Organization {
  return {
    ...VERIFIED,
    workflow_states: state
      ? ['simple_publication_workflow|published', `provider_workflow|${state}`]
      : ['simple_publication_workflow|published'],
  } as unknown as Organization;
}

function renderProvider(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <ProviderInfo content={content} className={className} />
    </Wrapper>,
  );
}

describe('ProviderInfo', () => {
  it('renders the address of the provider', () => {
    const { getByText } = renderProvider(VERIFIED);
    expect(getByText('Avenida Paulista 1636')).toBeTruthy();
    expect(getByText('Brazil')).toBeTruthy();
  });

  it('renders the services of the provider', () => {
    const { getByText, container } = renderProvider(VERIFIED);
    expect(getByText('Services')).toBeTruthy();
    expect(container.querySelectorAll('li.service-item').length).toBe(2);
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderProvider(VERIFIED, 'organizationInfoBlock');
    const el = container.querySelector('.provider-info');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('organizationInfoBlock')).toBe(true);
  });
});

describe('ProviderInfo badge', () => {
  it('is shown when the provider workflow says verified', () => {
    const { container } = renderProvider(VERIFIED);
    expect(container.querySelector('.verified-badge')).not.toBeNull();
  });

  it.each(['created', 'pending', 'listed', 'archived'])(
    'is hidden in the %s state',
    (state) => {
      const { container } = renderProvider(withState(state));
      expect(container.querySelector('.verified-badge')).toBeNull();
    },
  );

  it('is hidden when the workflow is not in the chain', () => {
    const { container } = renderProvider(withState(null));
    expect(container.querySelector('.verified-badge')).toBeNull();
  });

  it('is hidden when workflow_states is missing entirely', () => {
    const bare = { ...VERIFIED, workflow_states: undefined };
    const { container } = renderProvider(bare as unknown as Organization);
    expect(container.querySelector('.verified-badge')).toBeNull();
  });

  it('reads verified from the provider workflow only', () => {
    /* A `verified` state of any other workflow must not verify. */
    const elsewhere = {
      ...VERIFIED,
      workflow_states: [
        'simple_publication_workflow|published',
        'another_workflow|verified',
      ],
    } as unknown as Organization;
    const { container } = renderProvider(elsewhere);
    expect(container.querySelector('.verified-badge')).toBeNull();
  });
});

describe('ProviderInfo services block', () => {
  it('is omitted when the provider lists no services', () => {
    const none = { ...VERIFIED, services: [] } as unknown as Organization;
    const { queryByText } = renderProvider(none);
    expect(queryByText('Services')).toBeNull();
  });

  it('does not omit the address along with it', () => {
    const none = { ...VERIFIED, services: [] } as unknown as Organization;
    const { getByText } = renderProvider(none);
    expect(getByText('Address')).toBeTruthy();
  });

  it('survives a missing services field', () => {
    const bare = {
      '@id': '/acme',
      workflow_states: [],
    } as unknown as Organization;
    expect(() => renderProvider(bare)).not.toThrow();
  });
});
