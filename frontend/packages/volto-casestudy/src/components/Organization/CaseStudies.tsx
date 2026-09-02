import React from 'react';
import Image from '@plone/volto/components/theme/Image/Image';
import UniversalLink from '@plone/volto/components/manage/UniversalLink/UniversalLink';
import { defineMessages, useIntl } from 'react-intl';
import {
  getSummaryImageField,
  hasSummaryImage,
} from '@plone-collective/volto-casestudy/helpers/preview';
import type {
  CaseStudyRelations,
  CaseStudySummary,
} from '@plone-collective/volto-casestudy/types/content';
import './case-studies.scss';

const messages = defineMessages({
  provided: {
    id: 'organization_case_studies_provided',
    defaultMessage: 'Projects',
  },
  received: {
    id: 'organization_case_studies_received',
    defaultMessage: 'Case studies',
  },
});

/**
 * One case study: its screenshot, title and description, all inside a single
 * link to the case study itself.
 */
export const CaseStudyEntry: React.FC<{ item: CaseStudySummary }> = ({
  item,
}) => {
  if (!item?.['@id']) return null;

  return (
    <li className="case-study">
      <UniversalLink item={item} className="case-study-link">
        {hasSummaryImage(item) && (
          <span className="case-study-image">
            <Image
              item={item}
              imageField={getSummaryImageField(item)}
              // Decorative: the link is already labelled by the title next to
              // it, so naming the image again only doubles the announcement.
              alt=""
              loading="lazy"
              responsive
            />
          </span>
        )}
        <span className="case-study-body">
          <span className="case-study-title">{item.title}</span>
          {item.description && (
            <span className="case-study-description">{item.description}</span>
          )}
        </span>
      </UniversalLink>
    </li>
  );
};

interface CaseStudyGroupProps {
  items: CaseStudySummary[];
  title: string;
}

/** One titled group, rendered only when it has something in it. */
const CaseStudyGroup: React.FC<CaseStudyGroupProps> = ({ items, title }) => {
  if (!items?.length) return null;

  return (
    <section className="case-studies-group">
      <h2 className="case-studies-title">{title}</h2>
      <ul className="case-studies-list">
        {items.map((item) => (
          <CaseStudyEntry key={item['@id']} item={item} />
        ))}
      </ul>
    </section>
  );
};

export interface CaseStudiesProps {
  /** The organization's `case_studies`, as the REST API serializes them. */
  case_studies: CaseStudyRelations;
  /** Extra classes for the wrapper. */
  className?: string;
}

/**
 * List the case studies an organization takes part in.
 *
 * The two buckets are kept apart because they say different things: one is
 * work the organization delivered, the other is coverage of the organization
 * itself. An empty bucket is dropped, and an organization with neither
 * renders nothing at all rather than an empty heading.
 */
export const CaseStudies = ({ case_studies, className }: CaseStudiesProps) => {
  const intl = useIntl();
  const provided = case_studies?.provided ?? [];
  const received = case_studies?.received ?? [];

  if (!provided.length && !received.length) return null;

  const classes = className ? `case-studies ${className}` : 'case-studies';

  return (
    <div className={classes}>
      <CaseStudyGroup
        items={provided}
        title={intl.formatMessage(messages.provided)}
      />
      <CaseStudyGroup
        items={received}
        title={intl.formatMessage(messages.received)}
      />
    </div>
  );
};

export default CaseStudies;
