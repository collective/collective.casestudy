import React from 'react';
import cx from 'classnames';
import type { VocabularyTerm } from '@plone-collective/volto-casestudy/types/content';

export interface TermListProps {
  terms: VocabularyTerm[];
  /** Extra classes for the wrapper. */
  className?: string;
}

/**
 * Vocabulary terms as one comma-separated line. Renders inline, so it can
 * sit inside a paragraph.
 */
export const TermList = ({ terms, className }: TermListProps) => (
  <span className={cx('term-list', className)}>
    {terms.map((term, index) => (
      <span key={term.token || index} className={`term ${term.token}`}>
        {term.title}
        {index < terms.length - 1 ? ', ' : ''}
      </span>
    ))}
  </span>
);

export default TermList;
