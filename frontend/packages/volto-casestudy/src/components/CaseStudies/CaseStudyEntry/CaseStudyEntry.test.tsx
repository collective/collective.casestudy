import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import CaseStudyEntry from './CaseStudyEntry';
import type { CaseStudySummary } from '@plone-collective/volto-casestudy/types/content';

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

/** The entry is an `<li>`; give it the list its markup belongs in. */
function renderEntry(item: CaseStudySummary) {
  return render(
    <Wrapper anonymous>
      <ul>
        <CaseStudyEntry item={item} />
      </ul>
    </Wrapper>,
  );
}

describe('CaseStudyEntry', () => {
  it('renders the title', () => {
    const { container } = renderEntry(caseStudy('a', 'Plone.org'));
    expect(container.querySelector('.case-study-title')?.textContent).toBe(
      'Plone.org',
    );
  });

  it('renders the description', () => {
    const { getByText } = renderEntry(caseStudy('a', 'Plone.org'));
    expect(getByText('About Plone.org')).toBeTruthy();
  });

  it('omits the description element when there is none', () => {
    const { container } = renderEntry(
      caseStudy('a', 'Plone.org', { description: '' }),
    );
    expect(container.querySelector('.case-study-description')).toBeNull();
  });

  it('links to the case study', () => {
    const { container } = renderEntry(caseStudy('plone-org', 'Plone.org'));
    expect(
      container.querySelector('a.case-study-link')?.getAttribute('href'),
    ).toBe('/plone-org');
  });

  it('renders the screenshot from the summary', () => {
    const { container } = renderEntry(caseStudy('a', 'Plone.org', WITH_SHOT));
    const img = container.querySelector('.case-study-image img');
    // `download` is relative to the linked image, named by `base_path`.
    expect(img?.getAttribute('src')).toBe(
      '/screenshots/plone-org/@@images/image-400.png',
    );
  });

  it('leaves the screenshot out of the accessible name', () => {
    // The link already carries the title; naming the image repeats it.
    const { container } = renderEntry(caseStudy('a', 'Plone.org', WITH_SHOT));
    expect(
      container.querySelector('.case-study-image img')?.getAttribute('alt'),
    ).toBe('');
  });

  it('renders no image element when the case study has no screenshot', () => {
    const { container } = renderEntry(caseStudy('a', 'Plone.org'));
    expect(container.querySelector('.case-study-image')).toBeNull();
  });

  it('renders nothing when the case study has no resolvable path', () => {
    const { container } = renderEntry({
      ...caseStudy('a', 'Broken'),
      '@id': '',
    } as CaseStudySummary);
    expect(container.querySelector('.case-study')).toBeNull();
  });
});
