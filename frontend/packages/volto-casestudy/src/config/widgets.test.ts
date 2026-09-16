import { describe, it, expect } from 'vitest';
import type { ConfigType } from '@plone/registry';
import installWidgets, { TERMS_WIDGET } from './widgets';

/** A registry stub holding just what `installWidgets` touches. */
function makeConfig() {
  return {
    widgets: { widget: { text: 'TextWidget' } },
  } as unknown as ConfigType;
}

describe('installWidgets', () => {
  it('registers the widget the backend asks for by name', () => {
    const config = installWidgets(makeConfig());
    expect(config.widgets.widget[TERMS_WIDGET]).toBeTruthy();
  });

  it('keeps the widgets Volto already registered', () => {
    const config = installWidgets(makeConfig());
    expect(config.widgets.widget.text).toBeTruthy();
  });
});
