import { describe, it, expect } from 'vitest';
import { fromRows, termFromEntry, toRows } from './vocabularyTerms';

describe('termFromEntry', () => {
  it.each([
    [
      { token: 'gov', title: 'Government' },
      { token: 'gov', title: 'Government' },
    ],
    // Pre-2100 forms, still readable so an unmigrated site is editable.
    ['gov|Government', { token: 'gov', title: 'Government' }],
    ['6.2', { token: '6.2', title: '6.2' }],
    // Only the first separator splits, so a title may contain one.
    ['x|Design | Theming', { token: 'x', title: 'Design | Theming' }],
    // A stored object with no title falls back to the token.
    [{ token: 'gov' }, { token: 'gov', title: 'gov' }],
    [
      { token: 'gov', title: '' },
      { token: 'gov', title: 'gov' },
    ],
  ])('reads %o', (entry, expected) => {
    expect(termFromEntry(entry)).toEqual(expected);
  });

  it.each([
    [{}],
    [{ title: 'Government' }],
    [{ token: '' }],
    [''],
    ['|Government'],
    [null],
    [undefined],
    [42],
    [['gov', 'Government']],
  ])('drops %o', (entry) => {
    expect(termFromEntry(entry)).toBeUndefined();
  });
});

describe('toRows', () => {
  it('gives every row the id ObjectListWidget keys it by', () => {
    // Without it the widget calls `undefined.toString()` and the whole list
    // fails to render -- a control panel with no terms in it.
    expect(toRows([{ token: 'gov', title: 'Government' }])).toEqual([
      { '@id': '0', token: 'gov', title: 'Government' },
    ]);
  });

  it('numbers rows by position', () => {
    const rows = toRows([
      { token: 'a', title: 'A' },
      { token: 'b', title: 'B' },
    ]);
    expect(rows.map((r) => r['@id'])).toEqual(['0', '1']);
  });

  it('keeps record order', () => {
    const rows = toRows([
      { token: 'c', title: 'C' },
      { token: 'a', title: 'A' },
    ]);
    expect(rows.map((r) => r.token)).toEqual(['c', 'a']);
  });

  it('converts the pre-2100 shape', () => {
    expect(toRows(['gov|Government'])).toEqual([
      { '@id': '0', token: 'gov', title: 'Government' },
    ]);
  });

  it('reads a half-migrated record', () => {
    expect(
      toRows([{ token: 'gov', title: 'Government' }, 'edu|Education']),
    ).toEqual([
      { '@id': '0', token: 'gov', title: 'Government' },
      { '@id': '1', token: 'edu', title: 'Education' },
    ]);
  });

  it('keeps an incomplete row rather than dropping it', () => {
    // This runs on every keystroke, not only on load: a row the user just
    // added has no token yet and must not vanish under them.
    expect(toRows([{}])).toEqual([{ '@id': '0', token: '', title: '' }]);
  });

  it('renders junk as an empty, editable row', () => {
    expect(toRows([null, 42])).toEqual([
      { '@id': '0', token: '', title: '' },
      { '@id': '1', token: '', title: '' },
    ]);
  });

  it.each([[null], [undefined], ['not a list'], [{}], [42]])(
    'yields an empty list for %o',
    (value) => {
      expect(toRows(value)).toEqual([]);
    },
  );

  it('yields an empty list for an empty record', () => {
    expect(toRows([])).toEqual([]);
  });
});

describe('fromRows', () => {
  it('strips the row id the record must not store', () => {
    // The backend field validates with `additionalProperties: false`.
    expect(
      fromRows([{ '@id': '0', token: 'gov', title: 'Government' }]),
    ).toEqual([{ token: 'gov', title: 'Government' }]);
  });

  it('keeps row order', () => {
    const terms = fromRows([
      { '@id': '0', token: 'c', title: 'C' },
      { '@id': '1', token: 'a', title: 'A' },
    ]);
    expect(terms.map((t) => t.token)).toEqual(['c', 'a']);
  });

  it('passes an incomplete row through', () => {
    expect(fromRows([{ '@id': '0' }])).toEqual([{ token: '', title: '' }]);
  });

  it('round-trips a record unchanged', () => {
    const terms = [
      { token: 'gov', title: 'Government' },
      { token: 'edu', title: 'Education' },
    ];
    expect(fromRows(toRows(terms))).toEqual(terms);
  });

  it.each([[null], [undefined], ['not a list']])(
    'yields an empty list for %o',
    (value) => {
      expect(fromRows(value)).toEqual([]);
    },
  );
});
