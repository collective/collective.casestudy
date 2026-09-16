/*
 * Give the mocked config registry the `widgets.views` branch it lacks.
 *
 * Volto's `test-setup-config.jsx` replaces `widgets` wholesale with a mock
 * holding only the *edit* widget shape -- `id`, `widget`, `vocabulary`,
 * `type`, `choices`, `default` -- and no `views` key at all. The real app
 * never sees this: `installDefaultWidgets` (config/index.js) installs the
 * full mapping from config/Widgets.jsx, where `views.id` is a normal
 * namespace that Volto itself reads in helpers/Widget/widget.js.
 *
 * An add-on that registers a *view* widget therefore works in the app and
 * throws in tests. `@plonegovbr/volto-social-media` 3.0.0 started doing so
 * (`config.widgets.views.id.social_links`), which is supported usage; its
 * own suite passes because it hand-builds a config rather than using this
 * mock. Restoring the missing containers here keeps Volto's deliberately
 * mocked widgets intact and only adds what the mock forgot.
 *
 * This file runs after Volto's setup files, so it patches the mock rather
 * than being overwritten by it.
 */
import config from '@plone/volto/registry';

const views = config.widgets.views ?? {};

config.widgets.views = {
  ...views,
  id: { ...(views.id ?? {}) },
  widget: { ...(views.widget ?? {}) },
  vocabulary: { ...(views.vocabulary ?? {}) },
  type: { ...(views.type ?? {}) },
};
