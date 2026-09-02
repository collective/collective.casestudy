import { defineMessages } from 'react-intl';
import type { BlockSchemaProps, JSONSchema } from '@plone/types';

const messages = defineMessages({
  blockTitle: {
    id: 'Organization Settings',
    defaultMessage: 'Organization Settings',
  },
  settings: {
    id: 'Settings',
    defaultMessage: 'Settings',
  },
  source: {
    id: 'Source Organization',
    defaultMessage: 'Source Organization',
  },
  sourceDescription: {
    id: 'Leave empty to pull metadata from the current page.',
    defaultMessage: 'Leave empty to pull metadata from the current page.',
  },
});

export const OrganizationMetadataSchema = ({
  intl,
}: BlockSchemaProps): JSONSchema => ({
  title: intl.formatMessage(messages.blockTitle),
  fieldsets: [
    {
      id: 'default',
      title: intl.formatMessage(messages.settings),
      fields: ['organization_source'],
    },
  ],
  properties: {
    organization_source: {
      title: intl.formatMessage(messages.source),
      description: intl.formatMessage(messages.sourceDescription),
      widget: 'object_browser',
      mode: 'link',
      allowExternals: false,
      maximum: 1,
    },
  },
  required: [],
});

export default OrganizationMetadataSchema;
