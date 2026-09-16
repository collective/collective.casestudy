import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import OrganizationInfo from './OrganizationInfo';
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
 * the props this component passes, never that `AddressInfo` and
 * `IndustryInfo` can render them.
 */
const ACME = {
  '@id': 'http://localhost:8080/Plone/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  address: 'Avenida Paulista 1636',
  address_2: null,
  city: 'Sao Paulo',
  state: 'SP',
  postal_code: '01310-200',
  country: { token: 'BR', title: 'Brazil' },
  industry: { token: 'finance', title: 'Financial Services' },
  contact_name: 'Ada Lovelace',
  contact_email: 'ada@acme.example',
  services: [{ token: 'dev', title: 'Development' }],
} as unknown as Organization;

function renderInfo(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <OrganizationInfo content={content} className={className} />
    </Wrapper>,
  );
}

describe('OrganizationInfo', () => {
  it('renders the address of the organization', () => {
    const { getByText } = renderInfo(ACME);
    expect(getByText('Avenida Paulista 1636')).toBeTruthy();
    expect(getByText('Brazil')).toBeTruthy();
  });

  it('renders the industry of the organization', () => {
    const { getByText } = renderInfo(ACME);
    expect(getByText('Industry')).toBeTruthy();
    expect(getByText('Financial Services')).toBeTruthy();
  });

  it('renders neither contact nor services', () => {
    // Those two belong to `ProviderInfo`: an organization page shows where it
    // is and what it does, not who to call or what it sells.
    const { queryByText } = renderInfo(ACME);
    expect(queryByText('Contact')).toBeNull();
    expect(queryByText('Services')).toBeNull();
  });

  it('lays its children out as information blocks', () => {
    const { container } = renderInfo(ACME);
    expect(container.querySelector('.organizationInfoBlocks')).not.toBeNull();
    expect(
      container.querySelectorAll('.organizationInfoBlock').length,
    ).toBeGreaterThan(0);
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderInfo(ACME, 'mainInfoBlock');
    const el = container.querySelector('.organization-info');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('mainInfoBlock')).toBe(true);
  });

  it('drops a block whose fields are all empty', () => {
    const noIndustry = { ...ACME, industry: null } as unknown as Organization;
    const { container, getByText } = renderInfo(noIndustry);
    expect(container.querySelector('.industry-info')).toBeNull();
    // The address is unaffected by its neighbour dropping out.
    expect(getByText('Avenida Paulista 1636')).toBeTruthy();
  });

  it('survives content with no information fields at all', () => {
    const bare = { '@id': '/acme' } as unknown as Organization;
    expect(() => renderInfo(bare)).not.toThrow();
  });
});
