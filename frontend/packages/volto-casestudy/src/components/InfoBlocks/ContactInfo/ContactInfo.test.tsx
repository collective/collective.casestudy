import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import ContactInfo from './ContactInfo';
import type { Organization } from '../../../types/content';

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

const FULL = {
  '@id': 'http://localhost:8080/Plone/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  contact_name: 'Ada Lovelace',
  contact_email: 'ada@acme.example',
  contact_phone: '+55 11 5555-0100',
} as unknown as Organization;

/** Every contact field null, which is what an organization starts as. */
const EMPTY = {
  ...FULL,
  contact_name: null,
  contact_email: null,
  contact_phone: null,
} as unknown as Organization;

function renderContact(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <ContactInfo content={content} className={className} />
    </Wrapper>,
  );
}

describe('ContactInfo', () => {
  it('renders a heading', () => {
    const { getByText } = renderContact(FULL);
    expect(getByText('Contact')).toBeTruthy();
  });

  it('renders the contact name', () => {
    const { container } = renderContact(FULL);
    expect(container.querySelector('.contactName')?.textContent).toBe(
      'Ada Lovelace',
    );
  });

  it('renders the phone number', () => {
    const { container } = renderContact(FULL);
    expect(container.querySelector('.contactPhone')?.textContent).toBe(
      '+55 11 5555-0100',
    );
  });

  it('renders the email as a mailto link', () => {
    const { container } = renderContact(FULL);
    const link = container.querySelector('.contactEmail a');
    expect(link?.getAttribute('href')).toBe('mailto:ada@acme.example');
    expect(link?.textContent).toBe('ada@acme.example');
  });

  it('omits every field that is empty', () => {
    const only = { ...EMPTY, contact_phone: '+49 30 555 0100' };
    const { container } = renderContact(only as unknown as Organization);
    expect(container.querySelectorAll('.contactLine')).toHaveLength(1);
    expect(container.querySelector('.contactName')).toBeNull();
    expect(container.querySelector('.contactEmail')).toBeNull();
  });

  it('renders nothing when every field is empty', () => {
    // The component guards itself: an organization with no contact details
    // must not leave a bare heading behind.
    const { container } = renderContact(EMPTY);
    expect(container.querySelector('.contact-info')).toBeNull();
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderContact(FULL, 'providerInfoBlock');
    const el = container.querySelector('.contact-info');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('providerInfoBlock')).toBe(true);
  });

  it('survives content with no contact fields at all', () => {
    const bare = { '@id': '/acme' } as unknown as Organization;
    expect(() => renderContact(bare)).not.toThrow();
  });
});
