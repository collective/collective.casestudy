import type { BlockConfigBase } from '@plone/types';
import icon from '@plone/volto/icons/list-bullet.svg';
import ProviderMetadataView from './View';
import ProviderMetadataEdit from './Edit';

const ProviderBlockInfo: BlockConfigBase = {
  id: 'provider_metadata',
  title: 'Provider Metadata',
  view: ProviderMetadataView,
  edit: ProviderMetadataEdit,
  icon: icon,
  group: 'text',
  restricted: ({ contentType }) => {
    return contentType !== 'Provider';
  },
};

export default ProviderBlockInfo;
