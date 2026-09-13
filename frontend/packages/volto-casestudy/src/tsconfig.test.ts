import { describe, it, expect } from 'vitest';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const packageDir = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  '..',
);

function readJson(name: string) {
  return JSON.parse(readFileSync(path.join(packageDir, name), 'utf8'));
}

/**
 * The paths below resolve only inside this checkout, and they have to live in
 * `tsconfig.json` rather than a `tsconfig.dev.json` beside it: an IDE's
 * TypeScript service locates its project by walking up from the open file
 * looking for `tsconfig.json`, and offers no setting that names a different
 * file. A config under any other name is simply never read.
 *
 * That makes the shipped tarball, not the file's contents, the thing worth
 * guarding -- see the `npm pack` test below.
 */
describe('tsconfig.json', () => {
  const tsconfig = readJson('tsconfig.json');
  const paths: Record<string, string[]> = tsconfig.compilerOptions.paths;

  it('keeps the self-reference', () => {
    expect(paths['@plone-collective/volto-casestudy/*']).toEqual(['./src/*']);
  });

  it('resolves @plone/volto against the monorepo checkout', () => {
    // Volto's subpaths live under `src/`, and the package publishes no
    // `exports` map that would remap them, so node_modules resolution cannot
    // stand in for this entry.
    expect(paths['@plone/volto/*']).toEqual([
      '../../core/packages/volto/src/*',
    ]);
  });

  it('has no `extends`, so nothing depends on a second config file', () => {
    expect(tsconfig.extends).toBeUndefined();
  });
});

/**
 * Volto's `AddonRegistry` reads a *published* add-on's `tsconfig.json` and
 * spreads its `paths` over the aliases it has already resolved, so a
 * monorepo-relative entry would rewrite that alias for the consuming project
 * -- and for whichever unrelated package the entry names. It cannot fail
 * inside this checkout, because a workspace add-on never goes down that code
 * path, so nothing but this test stands between an edit and a broken release.
 *
 * Shipping no tsconfig at all is what makes that safe: `getTSConfigPaths`
 * finds no config file and `getAliasesFromTSConfig` guards with `options ||
 * {}`, so the add-on contributes zero aliases.
 *
 * This asserts against the real tarball rather than the `.npmignore` text,
 * which would still pass if `files` or `.npmignore` were restructured.
 */
describe('published tarball', () => {
  const files: string[] = JSON.parse(
    execFileSync('npm', ['pack', '--dry-run', '--json'], {
      cwd: packageDir,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }),
  )[0].files.map((f: { path: string }) => f.path);

  it('is not empty, so an empty listing cannot pass the checks below', () => {
    expect(files.length).toBeGreaterThan(10);
    expect(files).toContain('src/index.ts');
  });

  it('ships no TypeScript project config', () => {
    const configs = files.filter((f) =>
      /^(tsconfig|jsconfig)[^/]*\.json$/.test(f),
    );
    expect(configs).toEqual([]);
  });
}, 30_000);
