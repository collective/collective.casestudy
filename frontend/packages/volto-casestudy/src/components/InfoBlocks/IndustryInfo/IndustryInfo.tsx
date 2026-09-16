import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './industry-info.scss';

export interface IndustryInfoProps {
  content: Organization;
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
  const classes = ['industry-info'];
  if (className) classes.push(className);

  const industry = content?.industry;

  const display = industry;

  return (
    display && (
      <Container className={classes.join(' ')}>
        <h2 className="blockTitle industryTitle">
          {intl.formatMessage(messages.industry)}
        </h2>
        <p className="industryWrapper">
          <span className={`industryLine industry ${industry.token}`}>
            {industry.title}
          </span>
        </p>
      </Container>
    )
  );
};

export default IndustryInfo;
