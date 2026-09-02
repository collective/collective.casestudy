import type { BlockConfigBase, BlocksFormData } from '@plone/types';
import icon from '@plone/volto/icons/list-bullet.svg';
import OrganizationMetadataView from './View';
import OrganizationMetadataEdit from './Edit';
import { OrganizationMetadataSchema } from './schema';
import type { MetadataSource } from '../CaseStudyMetadata';

export type { MetadataSource };

export interface OrganizationMetadataData extends BlocksFormData {
  /** Empty means "use the current page". */
  organization_source?: MetadataSource[];
}

const OrganizationBlockInfo: BlockConfigBase = {
  id: 'organization_metadata',
  title: 'Organization Metadata',
  // `@plone/types` declares `Content['subjects']` as the empty tuple `[]`,
  // so a view whose `properties` is accurately typed is not assignable to
  // `BlockViewProps`. Cast until that is fixed upstream.
  view: OrganizationMetadataView as unknown as BlockConfigBase['view'],
  edit: OrganizationMetadataEdit,
  blockSchema: OrganizationMetadataSchema,
  icon: icon,
  group: 'text',
  mostUsed: false,
  sidebarTab: 1,
  restricted: ({ contentType }) => {
    return contentType !== 'Organization';
  },
};

export default OrganizationBlockInfo;
