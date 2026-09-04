import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import VocabularyTermsWidget, {
  vocabularyTermSchema,
} from './VocabularyTermsWidget';

const captured: Record<string, any> = {};

vi.mock('@plone/volto/components/manage/Widgets/ObjectListWidget', () => ({
  default: (props: Record<string, any>) => {
    Object.assign(captured, props);
    return <div data-testid="object-list" />;
  },
}));

vi.mock('react-intl', () => ({
  defineMessages: (messages: Record<string, unknown>) => messages,
  useIntl: () => ({
    formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
      defaultMessage,
  }),
}));

function renderWidget(value: unknown) {
  return render(
    <VocabularyTermsWidget id="industries" value={value} onChange={vi.fn()} />,
  );
}

describe('VocabularyTermsWidget', () => {
  it('edits the record with the object list widget', () => {
    const { getByTestId } = renderWidget([
      { token: 'gov', title: 'Government' },
    ]);
    expect(getByTestId('object-list')).toBeTruthy();
  });

  it('gives every row the id ObjectListWidget keys it by', () => {
    // Without `@id` the list calls `undefined.toString()` and renders nothing.
    renderWidget([{ token: 'gov', title: 'Government' }]);
    expect(captured.value).toEqual([
      { '@id': '0', token: 'gov', title: 'Government' },
    ]);
  });

  it('repairs a pre-2100 record so the panel stays editable', () => {
    renderWidget(['gov|Government', 'edu|Education']);
    expect(captured.value).toEqual([
      { '@id': '0', token: 'gov', title: 'Government' },
      { '@id': '1', token: 'edu', title: 'Education' },
    ]);
  });

  it('survives a record that is empty or absent', () => {
    renderWidget(undefined);
    expect(captured.value).toEqual([]);
  });

  it('keeps the field id the form gave it', () => {
    render(<VocabularyTermsWidget id="usages" value={[]} onChange={vi.fn()} />);
    expect(captured.id).toBe('usages');
  });

  it('strips the row id before handing the value back to the form', () => {
    // The backend record validates with `additionalProperties: false`.
    const onChange = vi.fn();
    render(
      <VocabularyTermsWidget id="usages" value={[]} onChange={onChange} />,
    );
    captured.onChange('usages', [
      { '@id': '0', token: 'gov', title: 'Government' },
    ]);
    expect(onChange).toHaveBeenCalledWith('usages', [
      { token: 'gov', title: 'Government' },
    ]);
  });

  it('passes an incomplete row through rather than dropping it', () => {
    // This runs on every keystroke; a row the user just added has no token.
    const onChange = vi.fn();
    render(
      <VocabularyTermsWidget id="usages" value={[]} onChange={onChange} />,
    );
    captured.onChange('usages', [{ '@id': '0' }]);
    expect(onChange).toHaveBeenCalledWith('usages', [{ token: '', title: '' }]);
  });

  it('describes a row as a token and a title', () => {
    renderWidget([]);
    expect(Object.keys(captured.schema.properties)).toEqual(['token', 'title']);
    expect(captured.schema.fieldsets[0].fields).toEqual(['token', 'title']);
  });

  it('requires both halves of a term', () => {
    renderWidget([]);
    expect(captured.schema.required).toEqual(['token', 'title']);
  });

  it('warns that the token is the half that must not change', () => {
    const schema = vocabularyTermSchema({
      formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
        defaultMessage,
    } as never);
    expect(schema.properties.token.description).toContain('orphans');
  });
});
