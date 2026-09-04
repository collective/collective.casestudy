/**
 * A term of one of this add-on's vocabulary settings records.
 *
 * Distinct from `VocabularyTerm` in `types/content`, which is a serialized
 * `Choice` value on a content item and whose title is optional.
 */
export interface SettingsTerm {
  token: string;
  title: string;
}

/** Separator of the pre-2100 `token|title` form. */
export const LEGACY_SEPARATOR = '|';

/**
 * Read one settings entry as a term.
 *
 * @param entry - An entry of a vocabulary record, in either the current
 *   object form or the pre-2100 string form.
 * @returns The term, or `undefined` when the entry carries no usable token.
 */
export function termFromEntry(entry: unknown): SettingsTerm | undefined {
  if (typeof entry === 'string') {
    // Pre-2100: "token|title", or a bare token used as its own title.
    const at = entry.indexOf(LEGACY_SEPARATOR);
    const token = at === -1 ? entry : entry.slice(0, at);
    if (!token) return undefined;
    const title = at === -1 ? '' : entry.slice(at + 1);
    return { token, title: title || token };
  }

  if (entry && typeof entry === 'object') {
    const { token, title } = entry as Partial<SettingsTerm>;
    if (!token) return undefined;
    return { token, title: title || token };
  }

  return undefined;
}

/**
 * A term as `ObjectListWidget` needs it.
 *
 * The widget keys every row by `@id` -- `childList={value.map((o) => [o['@id'], o])}`
 * -- so a row without one gets `undefined` as its drag id and is not rendered
 * at all. The id is presentation only: the backend record validates with
 * `additionalProperties: false` and would refuse it.
 */
export interface TermRow extends SettingsTerm {
  '@id': string;
}

/**
 * Read a settings record as editable rows.
 *
 * Deliberately lenient, because this sits inside the edit loop rather than
 * only at load: the form hands back whatever the widget last produced, so an
 * entry the user has started but not finished -- a row just added, with no
 * token yet -- has to survive the round trip instead of vanishing under them.
 * Dropping bad entries is the *vocabulary's* job, on read.
 *
 * Ids are positional. A token would be unstable, since editing one would
 * remount the row and take the caret with it.
 *
 * @param value - The record value, in any shape a site might hold.
 * @returns One row per entry, in record order.
 */
export function toRows(value: unknown): TermRow[] {
  if (!Array.isArray(value)) return [];
  return value.map((entry, index) => {
    const term = termFromEntry(entry);
    return {
      '@id': String(index),
      token: term?.token ?? '',
      title: term?.title ?? '',
    };
  });
}

/**
 * Turn edited rows back into what the record stores.
 *
 * Only `@id` is removed. An incomplete row is passed through rather than
 * dropped: this runs on every keystroke, and the backend is the thing that
 * decides whether a term is valid.
 *
 * @param rows - Rows as `ObjectListWidget` produced them.
 * @returns The terms to store, in row order.
 */
export function fromRows(rows: unknown): SettingsTerm[] {
  if (!Array.isArray(rows)) return [];
  return rows.map((row) => ({
    token: row?.token ?? '',
    title: row?.title ?? '',
  }));
}
