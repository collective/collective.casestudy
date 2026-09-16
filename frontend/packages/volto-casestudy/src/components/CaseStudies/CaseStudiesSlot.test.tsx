import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import CaseStudiesSlot from './CaseStudiesSlot';
import type {
  CaseStudySummary,
  Organization,
} from '@plone-collective/volto-casestudy/types/content';

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

function renderSlot(content: Partial<Organization>) {
  return render(
    <Wrapper anonymous>
      <CaseStudiesSlot content={content as Organization} />
    </Wrapper>,
  );
}

describe('CaseStudiesSlot', () => {
  it('renders the case studies carried by the content', () => {
    const { getByText } = renderSlot({
      case_studies: { provided: [CASE_STUDY], received: [] },
    });
    expect(getByText('New Plone.org')).toBeTruthy();
  });

  it('renders the band at full width', () => {
    // The slot always asks for the full-width treatment; the views used to
    // pass `full` themselves.
    const { container } = renderSlot({
      case_studies: { provided: [CASE_STUDY], received: [] },
    });
    expect(container.querySelector('.case-studies.full')).not.toBeNull();
  });

  it('keeps the two relations apart', () => {
    const { container } = renderSlot({
      case_studies: { provided: [CASE_STUDY], received: [CASE_STUDY] },
    });
    expect(container.querySelector('.case-studies.provided')).not.toBeNull();
    expect(container.querySelector('.case-studies.received')).not.toBeNull();
  });

  it('renders nothing when there are no case studies', () => {
    // The predicate normally keeps it from being rendered at all; this is the
    // belt to that braces.
    const { container } = renderSlot({
      case_studies: { provided: [], received: [] },
    });
    expect(container.querySelector('.case-studies')).toBeNull();
  });

  it('survives content with no case_studies key at all', () => {
    expect(() => renderSlot({})).not.toThrow();
  });
});
