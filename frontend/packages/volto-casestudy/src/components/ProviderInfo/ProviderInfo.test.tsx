import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import ProviderInfo from './ProviderInfo';
import type { Organization } from '../../types/content';

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
 * The children are rendered for real rather than mocked. A mock would assert
 * the props this component passes, never that `AddressInfo`, `ContactInfo`
 * and `ServicesInfo` can render them.
 */
const PROVIDER = {
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

function renderProvider(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <ProviderInfo content={content} className={className} />
    </Wrapper>,
  );
}

describe('ProviderInfo', () => {
  it('renders the address of the provider', () => {
    const { getByText } = renderProvider(PROVIDER);
    expect(getByText('Avenida Paulista 1636')).toBeTruthy();
    expect(getByText('Brazil')).toBeTruthy();
  });

  it('renders the services of the provider', () => {
    const { getByText, container } = renderProvider(PROVIDER);
    expect(getByText('Services')).toBeTruthy();
    expect(container.querySelectorAll('li.service-item').length).toBe(2);
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderProvider(PROVIDER, 'organizationInfoBlock');
    const el = container.querySelector('.provider-info');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('organizationInfoBlock')).toBe(true);
  });

  it('leaves the verified badge to the view around it', () => {
    // The badge moved to `ProviderView`; this component never renders it,
    // whatever the provider workflow says.
    const { container } = renderProvider(PROVIDER);
    expect(container.querySelector('.verified-badge')).toBeNull();
  });
});

describe('ProviderInfo services block', () => {
  it('is omitted when the provider lists no services', () => {
    const none = { ...PROVIDER, services: [] } as unknown as Organization;
    const { queryByText } = renderProvider(none);
    expect(queryByText('Services')).toBeNull();
  });

  it('does not omit the address along with it', () => {
    const none = { ...PROVIDER, services: [] } as unknown as Organization;
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
