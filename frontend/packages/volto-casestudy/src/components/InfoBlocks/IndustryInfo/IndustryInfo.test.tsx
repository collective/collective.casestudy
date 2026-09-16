import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import IndustryInfo from './IndustryInfo';
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

const ACME = {
  '@id': 'http://localhost:8080/Plone/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  industry: { token: 'finance', title: 'Financial Services' },
} as unknown as Organization;

function renderIndustry(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <IndustryInfo content={content} className={className} />
    </Wrapper>,
  );
}

describe('IndustryInfo', () => {
  it('renders a heading', () => {
    const { getByText } = renderIndustry(ACME);
    expect(getByText('Industry')).toBeTruthy();
  });

  it('renders the industry title, not its token', () => {
    const { getByText, queryByText } = renderIndustry(ACME);
    expect(getByText('Financial Services')).toBeTruthy();
    expect(queryByText('finance')).toBeNull();
  });

  it('marks the industry with its token as a class', () => {
    const { container } = renderIndustry(ACME);
    expect(container.querySelector('.industry.finance')).not.toBeNull();
  });

  it('renders nothing when the organization has no industry', () => {
    // The component guards itself: a bare heading with no value under it
    // would be worse than no block at all.
    const none = { ...ACME, industry: null } as unknown as Organization;
    const { container } = renderIndustry(none);
    expect(container.querySelector('.industry-info')).toBeNull();
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderIndustry(ACME, 'organizationInfoBlock');
    const el = container.querySelector('.industry-info');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('organizationInfoBlock')).toBe(true);
  });

  it('survives content with no industry field at all', () => {
    const bare = { '@id': '/acme' } as unknown as Organization;
    expect(() => renderIndustry(bare)).not.toThrow();
  });
});
