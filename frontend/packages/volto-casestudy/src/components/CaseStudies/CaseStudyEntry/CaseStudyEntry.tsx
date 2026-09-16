import React from 'react';
import Image from '@plone/volto/components/theme/Image/Image';
import UniversalLink from '@plone/volto/components/manage/UniversalLink/UniversalLink';
import {
  getSummaryImageField,
  hasSummaryImage,
} from '@plone-collective/volto-casestudy/helpers/preview';
import type { CaseStudySummary } from '@plone-collective/volto-casestudy/types/content';
import './case-study-entry.scss';

export interface CaseStudyEntryProps {
  /** One case study, as the REST API summarizes it. */
  item: CaseStudySummary;
}

/**
 * One case study: its screenshot, title and description, all inside a single
 * link to the case study itself.
 *
 * Rendered as a list item, so it belongs inside a list -- `CaseStudyGroup`
 * provides one.
 */
export const CaseStudyEntry: React.FC<CaseStudyEntryProps> = ({ item }) => {
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

export default CaseStudyEntry;
