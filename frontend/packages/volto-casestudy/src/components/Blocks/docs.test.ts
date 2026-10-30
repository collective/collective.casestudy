import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { createIntl } from 'react-intl';
import type { JSONSchema } from '@plone/types';
import CaseStudyBlockInfo from './CaseStudyMetadata';
import OrganizationBlockInfo from './OrganizationMetadata';

const blocksDir = path.dirname(fileURLToPath(import.meta.url));

const FRONTMATTER = /^---\n([\s\S]*?)\n---\n/;

/** Split a `*.block.md` file into its frontmatter and its Markdown. */
function readDocs(folder: string) {
  const file = readFileSync(
    path.join(blocksDir, folder, 'docs.block.md'),
    'utf8',
  );
  return {
    frontmatter: file.match(FRONTMATTER)?.[1] ?? '',
    markdown: file.replace(FRONTMATTER, '').trim(),
  };
}

/** Resolve a block's schema with the arguments `@blocks-schema` passes. */
function resolveSchema(block: typeof CaseStudyBlockInfo): JSONSchema {
  const intl = createIntl({ locale: 'en', messages: {}, onError: () => {} });
  const data = { '@type': block.id };
  return (block.blockSchema as (args: unknown) => JSONSchema)({
    data,
    intl,
    props: { data },
  });
}

describe.each([
  ['CaseStudyMetadata', CaseStudyBlockInfo],
  ['OrganizationMetadata', OrganizationBlockInfo],
] as const)('%s docs', (folder, block) => {
  const { frontmatter, markdown } = readDocs(folder);
  const schema = resolveSchema(block);
  const examples = [...markdown.matchAll(/```json\n([\s\S]*?)\n```/g)].map(
    ([, json]) => JSON.parse(json),
  );

  it('names the block by the id the registry keys it by', () => {
    expect(frontmatter).toBe(`block: ${block.id}`);
  });

  it('opens with a one-paragraph summary', () => {
    expect(markdown.split(/\n\s*\n/)[0]).toMatch(/^Shows the details of an? /);
  });

  it('nests its headings below the one the endpoint adds', () => {
    expect(markdown).not.toMatch(/^#{1,2} /m);
  });

  it('explains every field of the schema', () => {
    for (const field of Object.keys(schema.properties)) {
      expect(markdown).toContain(`- \`${field}\`: `);
    }
  });

  it('has a minimal example and one using every field', () => {
    expect(examples).toContainEqual({ '@type': block.id });
    expect(examples.flatMap(Object.keys)).toEqual(
      expect.arrayContaining(Object.keys(schema.properties)),
    );
  });

  it('only has examples that are data for this block', () => {
    const known = ['@type', ...Object.keys(schema.properties)];
    for (const example of examples) {
      expect(example['@type']).toBe(block.id);
      expect(known).toEqual(expect.arrayContaining(Object.keys(example)));
    }
  });
});
