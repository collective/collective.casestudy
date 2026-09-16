import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import CaseStudies from './CaseStudies';
import type {
  CaseStudyRelations,
  CaseStudySummary,
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

function caseStudy(id: string, title: string): CaseStudySummary {
  return {
    '@id': `http://localhost:8080/Plone/${id}`,
    '@type': 'CaseStudy',
    UID: `${id}-uid`,
    title,
    description: `About ${title}`,
    review_state: 'published',
    image_field: '',
    image_scales: null,
  } as unknown as CaseStudySummary;
}

const EMPTY: CaseStudyRelations = { provided: [], received: [] };

function renderList(case_studies: Partial<CaseStudyRelations>) {
  return render(
    <Wrapper anonymous>
      <CaseStudies case_studies={{ ...EMPTY, ...case_studies }} />
    </Wrapper>,
  );
}

describe('CaseStudies', () => {
  it('renders nothing when there are no case studies', () => {
    const { container } = renderList({});
    expect(container.querySelector('.case-studies')).toBeNull();
  });

  it('renders nothing when the prop is missing entirely', () => {
    const { container } = render(
      <Wrapper anonymous>
        <CaseStudies
          case_studies={undefined as unknown as CaseStudyRelations}
        />
      </Wrapper>,
    );
    expect(container.querySelector('.case-studies')).toBeNull();
  });

  it('shows only the group that has entries', () => {
    const { container, getByText, queryByText } = renderList({
      received: [caseStudy('a', 'Plone.org')],
    });
    expect(getByText('Case studies')).toBeTruthy();
    expect(queryByText('Projects')).toBeNull();
    expect(container.querySelectorAll('.case-studies-group')).toHaveLength(1);
  });

  it('keeps delivered and featured case studies apart', () => {
    const { container } = renderList({
      provided: [caseStudy('a', 'Delivered One')],
      received: [caseStudy('b', 'About Us')],
    });
    const groups = container.querySelectorAll('.case-studies-group');
    expect(groups).toHaveLength(2);
    // `provided` is rendered first: it is the organization's own work.
    expect(groups[0].querySelector('.case-study-title')?.textContent).toBe(
      'Delivered One',
    );
    expect(groups[1].querySelector('.case-study-title')?.textContent).toBe(
      'About Us',
    );
  });

  it('titles each group for what the relation means', () => {
    const { container } = renderList({
      provided: [caseStudy('a', 'Delivered One')],
      received: [caseStudy('b', 'About Us')],
    });
    const titles = Array.from(
      container.querySelectorAll('.case-studies-title'),
    ).map((el) => el.textContent);
    expect(titles).toEqual(['Projects', 'Case studies']);
  });

  it('passes a caller-supplied className through', () => {
    const { container } = render(
      <Wrapper anonymous>
        <CaseStudies
          case_studies={{ ...EMPTY, received: [caseStudy('a', 'Plone.org')] }}
          className="organization-case-studies"
        />
      </Wrapper>,
    );
    expect(
      container.querySelector('.case-studies.organization-case-studies'),
    ).toBeTruthy();
  });
});
