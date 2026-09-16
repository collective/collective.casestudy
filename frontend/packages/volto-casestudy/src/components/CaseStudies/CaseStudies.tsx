import { defineMessages, useIntl } from 'react-intl';
import CaseStudyGroup from '@plone-collective/volto-casestudy/components/CaseStudies/CaseStudyGroup/CaseStudyGroup';
import type { CaseStudyRelations } from '@plone-collective/volto-casestudy/types/content';
import { Container } from '@plone/components';
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

export interface CaseStudiesProps {
  /** The organization's `case_studies`, as the REST API serializes them. */
  case_studies: CaseStudyRelations;
  full?: boolean;
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
export const CaseStudies = ({
  case_studies,
  className,
  full = true,
}: CaseStudiesProps) => {
  const intl = useIntl();
  const provided = case_studies?.provided ?? [];
  const received = case_studies?.received ?? [];

  if (!provided.length && !received.length) return null;

  const classes = className
    ? `case-studies ${className} ${full ? 'full' : ''}`
    : `case-studies ${full ? 'full' : ''}`;

  return (
    <>
      {provided.length > 0 && (
        <Container className={`provided ${classes}`}>
          <CaseStudyGroup
            items={provided}
            title={intl.formatMessage(messages.provided)}
          />
        </Container>
      )}

      {received.length > 0 && (
        <Container className={`received ${classes}`}>
          <CaseStudyGroup
            items={received}
            title={intl.formatMessage(messages.received)}
          />
        </Container>
      )}
    </>
  );
};

export default CaseStudies;
