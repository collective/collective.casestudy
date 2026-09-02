import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const packageDir = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  '..',
);

function read(name: string) {
  return readFileSync(path.join(packageDir, name), 'utf8');
}

function readJson(name: string) {
  return JSON.parse(read(name));
}

/**
 * Volto's `AddonRegistry` reads a *published* add-on's `tsconfig.json` and
 * spreads its `paths` over the aliases it has already resolved, so a
 * monorepo-relative entry here rewrites that alias for the consuming project
 * -- and for whichever unrelated package the entry names. It cannot fail
 * inside this checkout, because a workspace add-on never goes down that code
 * path, so nothing but this test stands between an edit and a broken release.
 */
describe('shipped tsconfig.json', () => {
  const tsconfig = readJson('tsconfig.json');
  const paths: Record<string, string[]> = tsconfig.compilerOptions.paths;

  it('maps only this package', () => {
    expect(Object.keys(paths)).toEqual(['@plone-collective/volto-casestudy/*']);
  });

  it.each(Object.entries(paths))(
    '%s resolves inside the package',
    (_key, targets) => {
      for (const target of targets) {
        expect(target.startsWith('./src/')).toBe(true);
      }
    },
  );

  it('escapes neither the package nor into node_modules', () => {
    const targets = Object.values(paths).flat().join(' ');
    expect(targets).not.toContain('..');
    expect(targets).not.toContain('node_modules');
  });
});

describe('tsconfig.dev.json', () => {
  const dev = readJson('tsconfig.dev.json');

  it('extends the shipped config instead of replacing it', () => {
    expect(dev.extends).toBe('./tsconfig.json');
  });

  it('is where the monorepo-relative paths live', () => {
    expect(dev.compilerOptions.paths['@plone/volto/*']).toEqual([
      '../../core/packages/volto/src/*',
    ]);
  });

  it('keeps the self-reference, which `paths` would otherwise drop', () => {
    // `paths` is replaced wholesale by an extending config, not merged.
    expect(
      dev.compilerOptions.paths['@plone-collective/volto-casestudy/*'],
    ).toEqual(['./src/*']);
  });

  it('is kept out of the published tarball', () => {
    expect(read('.npmignore')).toContain('tsconfig.dev.json');
  });
});
