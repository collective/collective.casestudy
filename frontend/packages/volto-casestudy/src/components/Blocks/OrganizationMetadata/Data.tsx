import React from 'react';
import type { BlockEditProps } from '@plone/types';
import { BlockDataForm } from '@plone/volto/components/manage/Form';
import config from '@plone/volto/registry';
import { useIntl } from 'react-intl';
import { OrganizationMetadataSchema } from './schema';
import type { OrganizationMetadataData } from './index';

export interface OrganizationMetadataDataProps
  extends Partial<
    Pick<
      BlockEditProps,
      'blocksConfig' | 'blocksErrors' | 'contentType' | 'navRoot'
    >
  > {
  data: OrganizationMetadataData;
  block: string;
  onChangeBlock: (id: string, data: OrganizationMetadataData) => void;
}

const OrganizationMetadataDataForm: React.FC<OrganizationMetadataDataProps> = (
  props,
) => {
  const {
    data,
    block,
    blocksConfig = config.blocks.blocksConfig,
    blocksErrors,
    contentType,
    navRoot,
    onChangeBlock,
  } = props;
  const intl = useIntl();
  const blockSchema =
    blocksConfig?.[data['@type']]?.blockSchema ?? OrganizationMetadataSchema;
  const schema =
    typeof blockSchema === 'function'
      ? blockSchema({ ...props, intl } as any)
      : blockSchema;

  const handleFieldChange = (id: string, value: unknown) => {
    onChangeBlock(block, { ...data, [id]: value });
  };

  return (
    <BlockDataForm
      schema={schema}
      title={schema.title}
      onChangeField={handleFieldChange}
      onChangeBlock={onChangeBlock}
      formData={data}
      block={block}
      navRoot={navRoot}
      contentType={contentType}
      errors={blocksErrors}
    />
  );
};

export default OrganizationMetadataDataForm;
