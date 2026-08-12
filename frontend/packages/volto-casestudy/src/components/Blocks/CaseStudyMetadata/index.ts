import type { BlockConfigBase } from '@plone/types';
import icon from '@plone/volto/icons/list-bullet.svg';
import CaseStudyMetadataView from './View';
import CaseStudyMetadataEdit from './Edit';

const CaseStudyBlockInfo: BlockConfigBase = {
  id: 'case_study_metadata',
  title: 'Case Study Metadata',
  view: CaseStudyMetadataView,
  edit: CaseStudyMetadataEdit,
  icon: icon,
  group: 'text',
  restricted: ({ contentType }) => {
    return contentType !== 'CaseStudy';
  },
};

export default CaseStudyBlockInfo;
