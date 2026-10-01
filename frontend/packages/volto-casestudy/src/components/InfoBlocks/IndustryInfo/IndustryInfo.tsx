import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import InfoBox from '@plone-collective/volto-casestudy/components/InfoBlocks/InfoBox/InfoBox';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './industry-info.scss';

export interface IndustryInfoProps {
  /** Anything with an `industry` term -- an organization or a case study. */
  content: Pick<Organization, 'industry'>;
  /** Extra classes for the container. */
  className?: string;
}

const messages = defineMessages({
  industry: {
    id: 'Industry',
    defaultMessage: 'Industry',
  },
});

export const IndustryInfo = ({ content, className }: IndustryInfoProps) => {
  const intl = useIntl();
  const industry = content?.industry;
  if (!industry) return null;

  return (
    <InfoBox
      name="industry"
      title={intl.formatMessage(messages.industry)}
      className={className}
    >
      <span className={`industryLine industry ${industry.token}`}>
        {industry.title}
      </span>
    </InfoBox>
  );
};

export default IndustryInfo;
