import React from 'react';
import CaseStudyEntry from '@plone-collective/volto-casestudy/components/CaseStudies/CaseStudyEntry/CaseStudyEntry';
import type { CaseStudySummary } from '@plone-collective/volto-casestudy/types/content';
import './case-study-group.scss';

export interface CaseStudyGroupProps {
  /** The case studies to list. */
  items: CaseStudySummary[];
  /** Heading for the group, already translated by the caller. */
  title: string;
  /** Extra classes for the wrapper. */
  className?: string;
}

/** One titled group, rendered only when it has something in it. */
export const CaseStudyGroup: React.FC<CaseStudyGroupProps> = ({
  items,
  title,
  className,
}) => {
  if (!items?.length) return null;
  const classes = className ? `case-studies ${className}` : 'case-studies';

  return (
    <section className={`case-studies-group ${classes}`}>
      <h2 className="case-studies-title">{title}</h2>
      <ul className="case-studies-list">
        {items.map((item) => (
          <CaseStudyEntry key={item['@id']} item={item} />
        ))}
      </ul>
    </section>
  );
};

export default CaseStudyGroup;
