import { defineConfig } from 'vitest/config';
import voltoVitestConfig from '@plone/volto/vitest.config.mjs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const packageDir = path.dirname(fileURLToPath(import.meta.url));

/** Resolve an add-on's `src`, the way Volto's `AddonRegistry` aliases it. */
function addonSrc(name) {
  return path.join(path.dirname(require.resolve(`${name}/package.json`)), 'src');
}

const addonAlias = {
  '@plone-collective/volto-casestudy': path.resolve(packageDir, 'src'),
  '@plone/volto': path.resolve(packageDir, '../../core/packages/volto/src'),
  // Volto maps every add-on's package name onto its `src/` at build time.
  // vitest has no registry, so any add-on we import from needs the mapping
  // repeated here or the deep import resolves against the package root.
  '@plonegovbr/volto-social-media': addonSrc('@plonegovbr/volto-social-media'),
  '@plone-collective/volto-multiworkflow': addonSrc(
    '@plone-collective/volto-multiworkflow',
  ),
};

// `test.projects` each carry their own `resolve`, and a project's aliases win
// over the top-level ones — so the addon alias has to be merged into every
// project, not just the root config.
const projects = (voltoVitestConfig.test?.projects ?? []).map((project) => ({
  ...project,
  resolve: {
    ...project.resolve,
    alias: {
      ...(project.resolve?.alias ?? {}),
      ...addonAlias,
    },
  },
}));

export default defineConfig({
  ...voltoVitestConfig,
  resolve: {
    alias: {
      ...(voltoVitestConfig.resolve?.alias ?? {}),
      ...addonAlias,
    },
  },
  test: {
    ...voltoVitestConfig.test,
    projects,
  },
});
