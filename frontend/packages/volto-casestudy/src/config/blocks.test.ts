import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import installBlocks from './blocks';
import CaseStudyBlockInfo from '../components/Blocks/CaseStudyMetadata';
import OrganizationBlockInfo from '../components/Blocks/OrganizationMetadata';

/** A registry stub holding just what `installBlocks` touches. */
function makeConfig() {
  return {
    blocks: {
      blocksConfig: { title: { id: 'title' } },
      initialBlocks: { Document: ['title', 'text'] },
    },
  } as unknown as ConfigType;
}

describe('installBlocks', () => {
  it('registers both metadata blocks', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.blocksConfig.case_study_metadata).toBe(
      CaseStudyBlockInfo,
    );
    expect(config.blocks.blocksConfig.organization_metadata).toBe(
      OrganizationBlockInfo,
    );
  });

  it('keeps the blocks Volto already registered', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.blocksConfig.title).toBeTruthy();
  });

  it('starts a case study with title, description and its metadata', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.initialBlocks.CaseStudy).toEqual([
      'title',
      'description',
      'case_study_metadata',
    ]);
  });

  it('sets no initial blocks for organizations, which have none', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.initialBlocks.Organization).toBeUndefined();
  });

  it('does not drop initial blocks configured elsewhere', () => {
    const config = installBlocks(makeConfig());
    expect(config.blocks.initialBlocks.Document).toEqual(['title', 'text']);
  });
});
