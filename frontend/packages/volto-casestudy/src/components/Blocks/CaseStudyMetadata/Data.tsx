import React from 'react';
import { BlockDataForm } from '@plone/volto/components/manage/Form';
import { useIntl } from 'react-intl';
import { CaseStudyMetadataSchema } from './schema';
import type { CaseStudyMetadataData } from './index';

export interface CaseStudyMetadataDataProps {
  data: CaseStudyMetadataData;
  block: string;
  onChangeBlock: (id: string, data: CaseStudyMetadataData) => void;
}

const CaseStudyMetadataDataForm: React.FC<CaseStudyMetadataDataProps> = (
  props,
) => {
  const { data, block, onChangeBlock } = props;
  const intl = useIntl();
  const schema = CaseStudyMetadataSchema({ ...props, intl } as any);

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

export default CaseStudyMetadataDataForm;
