import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import AddressInfo from './AddressInfo';
import type { Organization } from '../../types/content';

const FULL = {
  '@id': 'http://localhost:8080/Plone/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  address: 'Avenida Paulista 1636',
  address_2: 'Sala 1504',
  city: 'Sao Paulo',
  state: 'SP',
  postal_code: '01310-200',
  country: { token: 'BR', title: 'Brazil' },
} as unknown as Organization;

/** Every address field null, which is what an organization starts as. */
const EMPTY = {
  ...FULL,
  address: null,
  address_2: null,
  city: null,
  state: null,
  postal_code: null,
  country: null,
} as unknown as Organization;

function renderAddress(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <AddressInfo content={content} className={className} />
    </Wrapper>,
  );
}

describe('AddressInfo', () => {
  it('renders a heading', () => {
    const { getByText } = renderAddress(FULL);
    expect(getByText('Address')).toBeTruthy();
  });

  it.each([
    ['address', 'Avenida Paulista 1636'],
    ['address_2', 'Sala 1504'],
    ['city', 'Sao Paulo'],
    ['state', 'SP'],
    ['postal code', '01310-200'],
  ])('renders the %s', (_label, value) => {
    const { getByText } = renderAddress(FULL);
    expect(getByText(value)).toBeTruthy();
  });

  it('renders the country title, not its token', () => {
    const { getByText, queryByText } = renderAddress(FULL);
    expect(getByText('Brazil')).toBeTruthy();
    expect(queryByText('BR')).toBeNull();
  });

  it('marks the country with its token as a class', () => {
    const { container } = renderAddress(FULL);
    expect(container.querySelector('.country.BR')).not.toBeNull();
  });

  it('omits every field that is empty', () => {
    const { container } = renderAddress(EMPTY);
    expect(container.querySelectorAll('.addressLine').length).toBe(0);
    expect(container.querySelectorAll('.addressInline').length).toBe(0);
  });

  it('still renders the heading with nothing to show', () => {
    const { getByText } = renderAddress(EMPTY);
    expect(getByText('Address')).toBeTruthy();
  });

  it('renders only the fields that are set', () => {
    const partial = { ...EMPTY, city: 'Berlin' } as unknown as Organization;
    const { getByText, container } = renderAddress(partial);
    expect(getByText('Berlin')).toBeTruthy();
    expect(container.querySelectorAll('.addressInline').length).toBe(1);
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderAddress(FULL, 'providerInfoBlock');
    const el = container.querySelector('.address-info');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('providerInfoBlock')).toBe(true);
  });

  it('survives content with no address fields at all', () => {
    const bare = { '@id': '/acme' } as unknown as Organization;
    expect(() => renderAddress(bare)).not.toThrow();
  });
});
