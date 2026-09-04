import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import CaseStudies from './CaseStudies';
import type { CaseStudyRelations, CaseStudySummary } from '../../types/content';

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

function caseStudy(
  id: string,
  title: string,
  extra: Partial<CaseStudySummary> = {},
): CaseStudySummary {
  return {
    '@id': `http://localhost:8080/Plone/${id}`,
    '@type': 'CaseStudy',
    UID: `${id}-uid`,
    title,
    description: `About ${title}`,
    review_state: 'published',
    image_field: '',
    image_scales: null,
    ...extra,
  } as unknown as CaseStudySummary;
}

const WITH_SHOT = {
  image_field: 'preview_image_link',
  image_scales: {
    preview_image_link: [
      {
        'content-type': 'image/png',
        download: '@@images/image-400.png',
        filename: 'shot.png',
        width: 400,
        height: 300,
        base_path: '/screenshots/plone-org',
        scales: {},
      },
    ],
  },
} as unknown as Partial<CaseStudySummary>;

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

  it('lists one entry per case study, in order', () => {
    const { container } = renderList({
      received: [caseStudy('a', 'Plone.org'), caseStudy('b', 'News Site')],
    });
    const titles = Array.from(
      container.querySelectorAll('.case-study-title'),
    ).map((el) => el.textContent);
    expect(titles).toEqual(['Plone.org', 'News Site']);
  });

  it('renders the description of each entry', () => {
    const { getByText } = renderList({
      received: [caseStudy('a', 'Plone.org')],
    });
    expect(getByText('About Plone.org')).toBeTruthy();
  });

  it('omits the description element when there is none', () => {
    const { container } = renderList({
      received: [caseStudy('a', 'Plone.org', { description: '' })],
    });
    expect(container.querySelector('.case-study-description')).toBeNull();
  });

  it('links each entry to the case study', () => {
    const { container } = renderList({
      received: [caseStudy('plone-org', 'Plone.org')],
    });
    expect(
      container.querySelector('a.case-study-link')?.getAttribute('href'),
    ).toBe('/plone-org');
  });

  it('renders the screenshot from the summary', () => {
    const { container } = renderList({
      received: [caseStudy('a', 'Plone.org', WITH_SHOT)],
    });
    const img = container.querySelector('.case-study-image img');
    // `download` is relative to the linked image, named by `base_path`.
    expect(img?.getAttribute('src')).toBe(
      '/screenshots/plone-org/@@images/image-400.png',
    );
  });

  it('leaves the screenshot out of the accessible name', () => {
    // The link already carries the title; naming the image repeats it.
    const { container } = renderList({
      received: [caseStudy('a', 'Plone.org', WITH_SHOT)],
    });
    expect(
      container.querySelector('.case-study-image img')?.getAttribute('alt'),
    ).toBe('');
  });

  it('renders no image element when the case study has no screenshot', () => {
    const { container } = renderList({
      received: [caseStudy('a', 'Plone.org')],
    });
    expect(container.querySelector('.case-study-image')).toBeNull();
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

  it('skips an entry with no resolvable path', () => {
    const { container } = renderList({
      received: [
        caseStudy('a', 'Plone.org'),
        { ...caseStudy('b', 'Broken'), '@id': '' } as CaseStudySummary,
      ],
    });
    expect(container.querySelectorAll('.case-study-link')).toHaveLength(1);
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
