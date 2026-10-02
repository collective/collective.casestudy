import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import type { ReactNode } from 'react';
import Wrapper from '@plone/volto/storybook';
import { CaseStudyMetadataView } from './View';
import type { CaseStudyMetadataData } from './index';
import type { CaseStudy, OrganizationSummary } from '../../../types/content';

vi.mock('react-intl', () => ({
  defineMessages: (messages: Record<string, unknown>) => messages,
  useIntl: () => ({
    formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
      defaultMessage,
  }),
  // `Wrapper` needs one; the mocked `formatMessage` above does the rest.
  IntlProvider: ({ children }: { children: ReactNode }) => children,
}));

function organization(id: string, title: string): OrganizationSummary {
  return {
    '@id': `http://localhost:8080/Plone/${id}`,
    '@type': 'Organization',
    UID: `${id}-uid`,
    title,
    description: '',
    review_state: 'published',
    image_field: '',
    image_scales: null,
  } as unknown as OrganizationSummary;
}

const BLOCK_DATA = { '@type': 'case_study_metadata' };

const baseContent = {
  '@id': 'http://localhost:8080/plone/a-case-study',
  '@type': 'CaseStudy',
  title: 'A Case Study',
  description: '',
  remoteUrl: '',
  preview_image_link: null,
  preview_caption_link: null,
  industry: null,
  usages: [],
  versions: [],
  organizations: [],
  providers: [],
  subjects: [],
} as unknown as CaseStudy;

const PREVIEW_IMAGE_LINK = {
  '@id': 'http://localhost:8080/plone/shot',
  image_scales: {
    image: [
      {
        download: '@@images/image-1-abc.png',
        width: 1200,
        height: 800,
        scales: {
          preview: {
            download: '@@images/image-preview.png',
            width: 400,
            height: 300,
          },
          great: {
            download: '@@images/image-great.png',
            width: 1200,
            height: 800,
          },
        },
      },
    ],
  },
} as any;

function renderView(
  content: Partial<CaseStudy>,
  data: CaseStudyMetadataData = BLOCK_DATA,
) {
  return render(
    <Wrapper anonymous>
      <CaseStudyMetadataView
        data={data}
        properties={{ ...baseContent, ...content } as CaseStudy}
      />
    </Wrapper>,
  );
}

describe('CaseStudyMetadataView', () => {
  it('renders nothing when there is no content', () => {
    const { container } = render(
      <CaseStudyMetadataView data={BLOCK_DATA} properties={undefined} />,
    );
    expect(container.firstChild).toBeNull();
  });

  it('links every related organization', () => {
    const { container } = renderView({
      organizations: [
        organization('acme', 'Acme Inc.'),
        organization('globex', 'Globex'),
      ],
    });
    const links = container.querySelectorAll(
      '.organization-list a.organization-link',
    );
    expect(Array.from(links).map((a) => a.textContent)).toEqual([
      'Acme Inc.',
      'Globex',
    ]);
    expect(links[0].getAttribute('href')).toBe('/acme');
  });

  it('lists providers separately from organizations', () => {
    const { container, getByText } = renderView({
      organizations: [organization('acme', 'Acme Inc.')],
      providers: [organization('agency', 'An Agency')],
    });
    expect(getByText('Organizations')).toBeTruthy();
    expect(getByText('Providers')).toBeTruthy();
    expect(container.querySelectorAll('.organization-list')).toHaveLength(2);
  });

  it('omits both sections when there are no relations', () => {
    const { container } = renderView({ organizations: [], providers: [] });
    expect(container.querySelector('.organization-list')).toBeNull();
  });

  it('renders the industry title', () => {
    const { getByText } = renderView({
      industry: { token: 'ngo', title: 'Non-government organization (NGO)' },
    });
    expect(getByText('Non-government organization (NGO)')).toBeTruthy();
  });

  it('joins usages with commas', () => {
    const { container } = renderView({
      usages: [
        { token: 'portal', title: 'Portal' },
        { token: 'intranet', title: 'Intranet' },
      ],
    });
    expect(container.textContent).toContain('Portal, Intranet');
  });

  it('does not leave a trailing comma on the last term', () => {
    const { container } = renderView({
      versions: [{ token: '6.0', title: 'Plone 6.0' }],
    });
    expect(container.textContent).toContain('Plone 6.0');
    expect(container.textContent).not.toContain('Plone 6.0,');
  });

  it('renders an external website link when remoteUrl is set', () => {
    const { container } = renderView({ remoteUrl: 'https://plone.org' });
    const link = container.querySelector('a');
    expect(link?.getAttribute('href')).toBe('https://plone.org');
    expect(link?.getAttribute('rel')).toBe('noopener noreferrer');
  });

  it('omits the website section when remoteUrl is empty', () => {
    const { container } = renderView({ remoteUrl: '' });
    expect(container.querySelector('a')).toBeNull();
  });

  it('renders the preview image at the great scale by default', () => {
    const { container } = renderView({
      preview_caption_link: 'A screenshot',
      preview_image_link: PREVIEW_IMAGE_LINK,
    });
    const img = container.querySelector('img.preview-image');
    expect(img?.getAttribute('src')).toBe(
      'http://localhost:8080/plone/shot/@@images/image-great.png',
    );
    expect(img?.getAttribute('alt')).toBe('A screenshot');
  });

  it('renders the preview image at the preview scale when compact', () => {
    const { container } = renderView(
      { preview_image_link: PREVIEW_IMAGE_LINK },
      { ...BLOCK_DATA, layout: 'compact' },
    );
    expect(
      container.querySelector('img.preview-image')?.getAttribute('src'),
    ).toBe('http://localhost:8080/plone/shot/@@images/image-preview.png');
  });

  it('renders no image when the relation is empty', () => {
    const { container } = renderView({ preview_image_link: null });
    expect(container.querySelector('img.preview-image')).toBeNull();
  });

  describe('layout', () => {
    const block = (container: HTMLElement) =>
      container.querySelector('.casestudy-metadata-block') as HTMLElement;

    it('defaults to the full-width layout', () => {
      const { container } = renderView({});
      expect(block(container).classList.contains('layout-full')).toBe(true);
      expect(block(container).classList.contains('floated')).toBe(false);
    });

    it('floats the compact layout to the right', () => {
      const { container } = renderView(
        {},
        { ...BLOCK_DATA, layout: 'compact' },
      );
      const classes = block(container).classList;
      expect(classes.contains('layout-compact')).toBe(true);
      expect(classes.contains('right')).toBe(true);
      expect(classes.contains('floated')).toBe(true);
    });

    it('falls back to full width for an unknown value', () => {
      const { container } = renderView({}, {
        ...BLOCK_DATA,
        layout: 'sideways',
      } as unknown as CaseStudyMetadataData);
      expect(block(container).classList.contains('layout-full')).toBe(true);
    });

    it('puts the image before the boxes', () => {
      const { container } = renderView({
        preview_image_link: PREVIEW_IMAGE_LINK,
      });
      const children = Array.from(block(container).children);
      expect(children.map((el) => el.className)).toEqual([
        'website-image',
        'metadata-boxes',
      ]);
    });

    it('renders one box per section, in order', () => {
      const { container } = renderView({
        organizations: [organization('acme', 'Acme Inc.')],
        providers: [organization('agency', 'An Agency')],
        industry: { token: 'ngo', title: 'NGO' },
        usages: [{ token: 'portal', title: 'Portal' }],
        versions: [{ token: '6.0', title: 'Plone 6.0' }],
        remoteUrl: 'https://plone.org',
        subjects: ['Tag 1'] as unknown as CaseStudy['subjects'],
      });
      const titles = container.querySelectorAll(
        '.metadata-boxes > .metadata-box.info-box > .blockTitle',
      );
      expect(Array.from(titles).map((h) => h.textContent)).toEqual([
        'Organizations',
        'Providers',
        'Industry',
        'Usage',
        'Versions',
        'Website',
        'What',
      ]);
      const ids = [
        'organizations',
        'providers',
        'industry',
        'usages',
        'versions',
        'website',
        'subjects',
      ];
      const boxes = container.querySelectorAll('.metadata-boxes > .info-box');
      Array.from(boxes).forEach((box, index) => {
        expect(box.classList.contains(ids[index])).toBe(true);
      });
      expect(boxes).toHaveLength(ids.length);
    });

    it('renders no boxes for empty sections', () => {
      const { container } = renderView({});
      expect(container.querySelectorAll('.metadata-box')).toHaveLength(0);
    });
  });
});
