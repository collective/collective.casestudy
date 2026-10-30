import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import CaseStudyMetadataDataForm from './Data';

vi.mock('@plone/volto/components/manage/Form', () => ({
  BlockDataForm: (props: {
    onChangeField: (id: string, value: unknown) => void;
    schema: { title: string };
  }) => {
    // Expose them so the test can inspect the wiring.
    (globalThis as any).__lastOnChangeField = props.onChangeField;
    (globalThis as any).__lastSchema = props.schema;
    (globalThis as any).__lastProps = props;
    return null;
  },
}));

vi.mock('@plone/volto/registry', () => ({
  default: { blocks: { blocksConfig: {} } },
}));

vi.mock('react-intl', () => ({
  defineMessages: (messages: Record<string, unknown>) => messages,
  useIntl: () => ({
    formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
      defaultMessage,
  }),
}));

describe('CaseStudyMetadataDataForm', () => {
  it('builds the schema with the source and layout fields', () => {
    render(
      <CaseStudyMetadataDataForm
        data={{ '@type': 'case_study_metadata' }}
        block="b"
        onChangeBlock={vi.fn()}
      />,
    );
    const schema = (globalThis as any).__lastSchema;
    expect(schema.title).toBe('Case Study Settings');
    expect(schema.fieldsets[0].fields).toEqual(['case_study_source', 'layout']);
    expect(schema.properties.case_study_source.widget).toBe('object_browser');
    expect(schema.properties.case_study_source.maximum).toBe(1);
  });

  it('offers full width as the default layout', () => {
    render(
      <CaseStudyMetadataDataForm
        data={{ '@type': 'case_study_metadata' }}
        block="b"
        onChangeBlock={vi.fn()}
      />,
    );
    const { layout } = (globalThis as any).__lastSchema.properties;
    expect(layout.default).toBe('full');
    expect(layout.choices.map(([value]: [string]) => value)).toEqual([
      'full',
      'compact',
    ]);
  });

  it('patches the changed field onto the existing data', () => {
    const onChangeBlock = vi.fn();
    render(
      <CaseStudyMetadataDataForm
        data={{ '@type': 'case_study_metadata' }}
        block="b"
        onChangeBlock={onChangeBlock}
      />,
    );
    const onChangeField = (globalThis as any).__lastOnChangeField;
    const source = [{ '@id': 'http://localhost:8080/plone/other' }];
    onChangeField('case_study_source', source);

    const [blockId, patch] = onChangeBlock.mock.calls[0];
    expect(blockId).toBe('b');
    expect(patch['@type']).toBe('case_study_metadata');
    expect(patch.case_study_source).toBe(source);
  });

  it('clears the source without dropping other keys', () => {
    const onChangeBlock = vi.fn();
    render(
      <CaseStudyMetadataDataForm
        data={{
          '@type': 'case_study_metadata',
          case_study_source: [{ '@id': 'http://localhost:8080/plone/x' }],
        }}
        block="b"
        onChangeBlock={onChangeBlock}
      />,
    );
    const onChangeField = (globalThis as any).__lastOnChangeField;
    onChangeField('case_study_source', []);

    const [, patch] = onChangeBlock.mock.calls[0];
    expect(patch.case_study_source).toEqual([]);
    expect(patch['@type']).toBe('case_study_metadata');
  });

  it('passes BlockDataForm what the core blocks pass it', () => {
    const onChangeBlock = vi.fn();
    const navRoot = { '@id': '/' } as any;
    const blocksErrors = { b: { layout: ['Required'] } };
    render(
      <CaseStudyMetadataDataForm
        data={{ '@type': 'case_study_metadata' }}
        block="b"
        onChangeBlock={onChangeBlock}
        navRoot={navRoot}
        contentType="CaseStudy"
        blocksErrors={blocksErrors}
      />,
    );
    const props = (globalThis as any).__lastProps;
    expect(props.onChangeBlock).toBe(onChangeBlock);
    expect(props.navRoot).toBe(navRoot);
    expect(props.contentType).toBe('CaseStudy');
    expect(props.errors).toBe(blocksErrors);
  });

  it('uses the schema from the block configuration', () => {
    const schema = { title: 'Customized', fieldsets: [], properties: {} };
    render(
      <CaseStudyMetadataDataForm
        data={{ '@type': 'case_study_metadata' }}
        block="b"
        onChangeBlock={vi.fn()}
        blocksConfig={
          { case_study_metadata: { blockSchema: () => schema } } as any
        }
      />,
    );
    expect((globalThis as any).__lastSchema).toBe(schema);
  });
});
