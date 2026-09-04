import type { BlockConfigBase, BlocksFormData } from '@plone/types';
import icon from '@plone/volto/icons/list-bullet.svg';
import CaseStudyMetadataView from './View';
import CaseStudyMetadataEdit from './Edit';
import { CaseStudyMetadataSchema } from './schema';

/** One item picked with the `object_browser` widget in `mode: 'link'`. */
export interface MetadataSource {
  '@id': string;
  title?: string;
  '@type'?: string;
}

export interface CaseStudyMetadataData extends BlocksFormData {
  /** Empty means "use the current page". */
  case_study_source?: MetadataSource[];
}

const CaseStudyBlockInfo: BlockConfigBase = {
  id: 'case_study_metadata',
  title: 'Case Study Metadata',
  // `@plone/types` declares `Content['subjects']` as the empty tuple `[]`,
  // so a view whose `properties` is accurately typed is not assignable to
  // `BlockViewProps`. Cast until that is fixed upstream.
  view: CaseStudyMetadataView as unknown as BlockConfigBase['view'],
  edit: CaseStudyMetadataEdit,
  blockSchema: CaseStudyMetadataSchema,
  icon: icon,
  group: 'text',
  mostUsed: false,
  sidebarTab: 1,
  restricted: ({ contentType }) => {
    return contentType !== 'CaseStudy';
  },
};

export default CaseStudyBlockInfo;
