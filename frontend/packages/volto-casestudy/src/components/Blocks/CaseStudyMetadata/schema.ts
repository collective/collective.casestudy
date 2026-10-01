import { defineMessages } from 'react-intl';
import type { BlockSchemaProps, JSONSchema } from '@plone/types';
import { DEFAULT_LAYOUT } from './layout';

const messages = defineMessages({
  blockTitle: {
    id: 'Case Study Settings',
    defaultMessage: 'Case Study Settings',
  },
  settings: {
    id: 'Settings',
    defaultMessage: 'Settings',
  },
  source: {
    id: 'Source Case Study',
    defaultMessage: 'Source Case Study',
  },
  sourceDescription: {
    id: 'Leave empty to pull metadata from the current page.',
    defaultMessage: 'Leave empty to pull metadata from the current page.',
  },
  layout: {
    id: 'Layout',
    defaultMessage: 'Layout',
  },
  layoutFull: {
    id: 'Full width',
    defaultMessage: 'Full width',
  },
  layoutCompact: {
    id: 'Compact (floated right)',
    defaultMessage: 'Compact (floated right)',
  },
});

export const CaseStudyMetadataSchema = ({
  intl,
}: BlockSchemaProps): JSONSchema => ({
  title: intl.formatMessage(messages.blockTitle),
  fieldsets: [
    {
      id: 'default',
      title: intl.formatMessage(messages.settings),
      fields: ['case_study_source', 'layout'],
    },
  ],
  properties: {
    layout: {
      title: intl.formatMessage(messages.layout),
      choices: [
        ['full', intl.formatMessage(messages.layoutFull)],
        ['compact', intl.formatMessage(messages.layoutCompact)],
      ],
      default: DEFAULT_LAYOUT,
      noValueOption: false,
    },
    case_study_source: {
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

export default CaseStudyMetadataSchema;
