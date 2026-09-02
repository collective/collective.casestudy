import { describe, it, expect } from 'vitest';
import CaseStudyBlockInfo from './CaseStudyMetadata';
import OrganizationBlockInfo from './OrganizationMetadata';

/** `restricted` is typed against Volto's full argument object. */
const restricted = (
  block: typeof CaseStudyBlockInfo,
  contentType: string,
): boolean =>
  (block.restricted as (args: { contentType: string }) => boolean)({
    contentType,
  });

describe.each([
  ['CaseStudyMetadata', CaseStudyBlockInfo, 'case_study_metadata', 'CaseStudy'],
  [
    'OrganizationMetadata',
    OrganizationBlockInfo,
    'organization_metadata',
    'Organization',
  ],
] as const)('%s block', (_name, block, id, contentType) => {
  it('declares the id the registry keys it by', () => {
    expect(block.id).toBe(id);
  });

  it('has a view, an edit component and a schema', () => {
    expect(block.view).toBeTruthy();
    expect(block.edit).toBeTruthy();
    expect(block.blockSchema).toBeTruthy();
  });

  it('is offered on its own content type', () => {
    expect(restricted(block, contentType)).toBe(false);
  });

  it('is hidden everywhere else', () => {
    expect(restricted(block, 'Document')).toBe(true);
    expect(restricted(block, 'News Item')).toBe(true);
  });

  it('edits from the first sidebar tab', () => {
    // The block has no inline controls, so its settings live in the sidebar.
    expect(block.sidebarTab).toBe(1);
  });

  it('is not promoted in the block chooser', () => {
    expect(block.mostUsed).toBe(false);
  });
});

describe('block ids', () => {
  it('are distinct, so one does not overwrite the other', () => {
    expect(CaseStudyBlockInfo.id).not.toBe(OrganizationBlockInfo.id);
  });

  it('are each restricted to a different content type', () => {
    expect(restricted(CaseStudyBlockInfo, 'Organization')).toBe(true);
    expect(restricted(OrganizationBlockInfo, 'CaseStudy')).toBe(true);
  });
});
