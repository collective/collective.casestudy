import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import OrganizationMetadataDataForm from './Data';

vi.mock('@plone/volto/components/manage/Form', () => ({
  BlockDataForm: ({
    onChangeField,
    schema,
  }: {
    onChangeField: (id: string, value: unknown) => void;
    schema: { title: string };
  }) => {
    (globalThis as any).__lastOnChangeField = onChangeField;
    (globalThis as any).__lastSchema = schema;
    return null;
  },
}));

vi.mock('react-intl', () => ({
  defineMessages: (messages: Record<string, unknown>) => messages,
  useIntl: () => ({
    formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
      defaultMessage,
  }),
}));

describe('OrganizationMetadataDataForm', () => {
  it('builds the schema with the source field', () => {
    render(
      <OrganizationMetadataDataForm
        data={{ '@type': 'organization_metadata' }}
        block="b"
        onChangeBlock={vi.fn()}
      />,
    );
    const schema = (globalThis as any).__lastSchema;
    expect(schema.title).toBe('Organization Settings');
    expect(schema.fieldsets[0].fields).toEqual(['organization_source']);
    expect(schema.properties.organization_source.widget).toBe('object_browser');
    expect(schema.properties.organization_source.maximum).toBe(1);
  });

  it('patches the changed field onto the existing data', () => {
    const onChangeBlock = vi.fn();
    render(
      <OrganizationMetadataDataForm
        data={{ '@type': 'organization_metadata' }}
        block="b"
        onChangeBlock={onChangeBlock}
      />,
    );
    const onChangeField = (globalThis as any).__lastOnChangeField;
    const source = [{ '@id': 'http://localhost:8080/plone/company-2' }];
    onChangeField('organization_source', source);

    const [blockId, patch] = onChangeBlock.mock.calls[0];
    expect(blockId).toBe('b');
    expect(patch['@type']).toBe('organization_metadata');
    expect(patch.organization_source).toBe(source);
  });

  it('clears the source without dropping other keys', () => {
    const onChangeBlock = vi.fn();
    render(
      <OrganizationMetadataDataForm
        data={{
          '@type': 'organization_metadata',
          organization_source: [{ '@id': 'http://localhost:8080/plone/x' }],
        }}
        block="b"
        onChangeBlock={onChangeBlock}
      />,
    );
    const onChangeField = (globalThis as any).__lastOnChangeField;
    onChangeField('organization_source', []);

    const [, patch] = onChangeBlock.mock.calls[0];
    expect(patch.organization_source).toEqual([]);
    expect(patch['@type']).toBe('organization_metadata');
  });
});
