import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import ObjectListWidget from '@plone/volto/components/manage/Widgets/ObjectListWidget';
import {
  fromRows,
  toRows,
} from '@plone-collective/volto-casestudy/helpers/vocabularyTerms';
import type {
  SettingsTerm,
  TermRow,
} from '@plone-collective/volto-casestudy/helpers/vocabularyTerms';

const messages = defineMessages({
  term: { id: 'vocabulary_term', defaultMessage: 'Term' },
  token: { id: 'vocabulary_term_token', defaultMessage: 'Token' },
  tokenDescription: {
    id: 'vocabulary_term_token_description',
    defaultMessage:
      'Stored on the content. Changing it orphans the content already using it.',
  },
  title: { id: 'vocabulary_term_title', defaultMessage: 'Title' },
  titleDescription: {
    id: 'vocabulary_term_title_description',
    defaultMessage: 'Shown to editors and visitors. Safe to change.',
  },
});

type Intl = ReturnType<typeof useIntl>;

/** Schema of one row, handed to Volto's `ObjectListWidget`. */
export const vocabularyTermSchema = (intl: Intl) => ({
  title: intl.formatMessage(messages.term),
  fieldsets: [
    {
      id: 'default',
      title: intl.formatMessage(messages.term),
      fields: ['token', 'title'],
    },
  ],
  properties: {
    token: {
      title: intl.formatMessage(messages.token),
      description: intl.formatMessage(messages.tokenDescription),
      type: 'string',
    },
    title: {
      title: intl.formatMessage(messages.title),
      description: intl.formatMessage(messages.titleDescription),
      type: 'string',
    },
  },
  required: ['token', 'title'],
});

export interface VocabularyTermsWidgetProps {
  id: string;
  value?: unknown;
  onChange: (id: string, value: SettingsTerm[]) => void;
  [key: string]: any;
}

/**
 * Edit one of this add-on's vocabulary settings records.
 *
 * The record is a `JSONField` holding an ordered array of `{token, title}`,
 * which is what `ObjectListWidget` edits -- so this is a row schema plus the
 * `@id` the widget keys its rows by, added here and stripped again before the
 * value goes back to the form. Without the add-on the control panel falls
 * back to Volto's raw JSON editor, which still works.
 */
const VocabularyTermsWidget: React.FC<VocabularyTermsWidgetProps> = (props) => {
  const intl = useIntl();
  const { onChange } = props;

  const handleChange = React.useCallback(
    (fieldId: string, rows: TermRow[]) => onChange(fieldId, fromRows(rows)),
    [onChange],
  );

  return (
    <ObjectListWidget
      {...props}
      value={toRows(props.value)}
      schema={vocabularyTermSchema(intl)}
      onChange={handleChange}
    />
  );
};

export default VocabularyTermsWidget;
