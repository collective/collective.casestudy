/**
 * The widget against the *real* `ObjectListWidget`.
 *
 * The unit tests next door mock it, which is what let the first version of
 * this widget ship a value `ObjectListWidget` cannot render: it keys every
 * row by `@id` and calls `childId.toString()`, so a row without one throws
 * and takes the whole list down -- a control panel showing a label, an "Add"
 * button and nothing else.
 *
 * `DragDropList` is lazy-loaded, so rows only render once the loadables are
 * primed; that is what `__setLoadables` is for.
 */
import { describe, it, expect, beforeAll, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import VocabularyTermsWidget from './VocabularyTermsWidget';

vi.mock('@plone/volto/helpers/Loadable/Loadable');
vi.mock('@plone/volto/components/manage/Form');

beforeAll(async () => {
  const { __setLoadables } = await import(
    '@plone/volto/helpers/Loadable/Loadable'
  );
  await __setLoadables();
});

const TERMS = [
  { token: 'gov', title: 'Government' },
  { token: 'edu', title: 'Education' },
  { token: 'ngo', title: 'NGO' },
];

function renderWidget(value: unknown, onChange = vi.fn()) {
  const result = render(
    <Wrapper anonymous>
      <VocabularyTermsWidget
        id="industries"
        title="Industries"
        value={value}
        onChange={onChange}
      />
    </Wrapper>,
  );
  return { ...result, onChange };
}

describe('VocabularyTermsWidget with the real ObjectListWidget', () => {
  it('renders one row per term', () => {
    const { container } = renderWidget(TERMS);
    expect(container.querySelectorAll('.accordion')).toHaveLength(TERMS.length);
  });

  it('renders rows for a pre-2100 record too', () => {
    const { container } = renderWidget(['gov|Government', 'edu|Education']);
    expect(container.querySelectorAll('.accordion')).toHaveLength(2);
  });

  it('renders no rows for an empty record, without throwing', () => {
    const { container } = renderWidget([]);
    expect(container.querySelectorAll('.accordion')).toHaveLength(0);
    expect(container.textContent).toContain('Add');
  });

  it('gives every row the id ObjectListWidget keys it by', () => {
    // The regression this file exists for: `childId.toString()` on a row
    // without `@id` throws, and the list renders nothing at all.
    const { container } = renderWidget(TERMS);
    const ids = Array.from(
      container.querySelectorAll('[data-rbd-draggable-id]'),
    ).map((el) => el.getAttribute('data-rbd-draggable-id'));
    expect(ids).toEqual(['0', '1', '2']);
  });

  it('strips the row id before handing the value back to the form', () => {
    // `additionalProperties: false` on the backend record would refuse it.
    const { container, onChange } = renderWidget(TERMS);
    const addButton = container.querySelector('button');
    addButton?.click();

    expect(onChange).toHaveBeenCalled();
    const [, value] = onChange.mock.calls[0];
    for (const term of value) {
      expect(Object.keys(term).sort()).toEqual(['title', 'token']);
    }
  });

  it('keeps a freshly added row instead of dropping it as incomplete', () => {
    const { container, onChange } = renderWidget(TERMS);
    container.querySelector('button')?.click();

    const [, value] = onChange.mock.calls[0];
    expect(value).toHaveLength(TERMS.length + 1);
    expect(value[TERMS.length]).toEqual({ token: '', title: '' });
  });
});
