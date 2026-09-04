import React from 'react';
import { BlockDataForm } from '@plone/volto/components/manage/Form';
import { useIntl } from 'react-intl';
import { OrganizationMetadataSchema } from './schema';
import type { OrganizationMetadataData } from './index';

export interface OrganizationMetadataDataProps {
  data: OrganizationMetadataData;
  block: string;
  onChangeBlock: (id: string, data: OrganizationMetadataData) => void;
}

const OrganizationMetadataDataForm: React.FC<OrganizationMetadataDataProps> = (
  props,
) => {
  const { data, block, onChangeBlock } = props;
  const intl = useIntl();
  const schema = OrganizationMetadataSchema({ ...props, intl } as any);

  const handleFieldChange = (id: string, value: unknown) => {
    onChangeBlock(block, { ...data, [id]: value });
  };

  return (
    <BlockDataForm
      schema={schema}
      title={schema.title}
      onChangeField={handleFieldChange}
      formData={data}
      block={block}
    />
  );
};

export default OrganizationMetadataDataForm;
