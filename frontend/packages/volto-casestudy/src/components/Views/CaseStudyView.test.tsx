import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import CaseStudyView from './CaseStudyView';
import type { CaseStudy } from '../../types/content';

vi.mock('@plone/volto/components/theme/View/RenderBlocks', () => ({
  default: ({ path }: { path: string }) => (
    <div data-testid="render-blocks" data-path={path} />
  ),
}));

const content = {
  '@id': 'http://localhost:8080/Plone/plone-org',
  '@type': 'CaseStudy',
  title: 'New Plone.org',
  description: '',
  blocks: {},
  blocks_layout: { items: [] },
} as unknown as CaseStudy;

function renderView(pathname?: string) {
  return render(
    <Wrapper anonymous>
      <CaseStudyView
        content={content}
        location={pathname === undefined ? undefined : { pathname }}
      />
    </Wrapper>,
  );
}

describe('CaseStudyView', () => {
  it('renders the blocks of the case study', () => {
    const { getByTestId } = renderView('/plone-org');
    expect(getByTestId('render-blocks')).toBeTruthy();
  });

  it('passes the content path down to the blocks renderer', () => {
    const { getByTestId } = renderView('/plone-org');
    expect(getByTestId('render-blocks').getAttribute('data-path')).toBe(
      '/plone-org',
    );
  });

  it('strips a non-content route off the path', () => {
    // `/edit` is a Volto route, not part of the content path -- blocks must
    // resolve against the object either way.
    const { getByTestId } = renderView('/plone-org/edit');
    expect(getByTestId('render-blocks').getAttribute('data-path')).toBe(
      '/plone-org',
    );
  });

  it('tolerates a missing location', () => {
    const { getByTestId } = renderView(undefined);
    expect(getByTestId('render-blocks').getAttribute('data-path')).toBe('');
  });

  it('marks the wrapper as the case study view', () => {
    const { container } = renderView('/plone-org');
    const wrapper = container.querySelector('#page-document');
    expect(wrapper?.className).toContain('casestudy-view');
  });
});
