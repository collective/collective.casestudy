import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import installViews from './views';

/** A registry stub holding just what `installViews` touches. */
function makeConfig() {
  return {
    views: {
      contentTypesViews: { Document: 'DocumentView' },
      layoutViews: { document_view: 'DocumentView' },
    },
  } as unknown as ConfigType;
}

describe('installViews', () => {
  it('registers a view for each content type', () => {
    const config = installViews(makeConfig());
    expect(config.views.contentTypesViews.CaseStudy).toBeTruthy();
    expect(config.views.contentTypesViews.Organization).toBeTruthy();
  });

  it('keeps the views Volto already registered', () => {
    const config = installViews(makeConfig());
    expect(config.views.contentTypesViews.Document).toBe('DocumentView');
    expect(config.views.layoutViews.document_view).toBe('DocumentView');
  });

  it('survives a registry with no views at all', () => {
    const config = installViews({} as unknown as ConfigType);
    expect(config.views.contentTypesViews.CaseStudy).toBeTruthy();
  });
});
