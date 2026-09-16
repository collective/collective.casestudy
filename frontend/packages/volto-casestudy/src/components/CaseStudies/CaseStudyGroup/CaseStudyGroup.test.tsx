import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import CaseStudyGroup from './CaseStudyGroup';
import type { CaseStudySummary } from '@plone-collective/volto-casestudy/types/content';

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

function renderGroup(items: CaseStudySummary[], title = 'Case studies') {
  return render(
    <Wrapper anonymous>
      <CaseStudyGroup items={items} title={title} />
    </Wrapper>,
  );
}

describe('CaseStudyGroup', () => {
  it('renders nothing when the group is empty', () => {
    const { container } = renderGroup([]);
    expect(container.querySelector('.case-studies-group')).toBeNull();
  });

  it('renders nothing when there are no items at all', () => {
    const { container } = render(
      <Wrapper anonymous>
        <CaseStudyGroup
          items={undefined as unknown as CaseStudySummary[]}
          title="Case studies"
        />
      </Wrapper>,
    );
    expect(container.querySelector('.case-studies-group')).toBeNull();
  });

  it('renders the title as a heading', () => {
    const { container } = renderGroup(
      [caseStudy('a', 'Plone.org')],
      'Projects',
    );
    expect(container.querySelector('h2.case-studies-title')?.textContent).toBe(
      'Projects',
    );
  });

  it('lists one entry per case study, in order', () => {
    const { container } = renderGroup([
      caseStudy('a', 'Plone.org'),
      caseStudy('b', 'News Site'),
    ]);
    const titles = Array.from(
      container.querySelectorAll('.case-studies-list .case-study-title'),
    ).map((el) => el.textContent);
    expect(titles).toEqual(['Plone.org', 'News Site']);
  });

  it('skips an entry with no resolvable path', () => {
    const { container } = renderGroup([
      caseStudy('a', 'Plone.org'),
      { ...caseStudy('b', 'Broken'), '@id': '' } as CaseStudySummary,
    ]);
    expect(container.querySelectorAll('.case-study-link')).toHaveLength(1);
  });
});
