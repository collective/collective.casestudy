import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './services-info.scss';

export interface ServicesInfoProps {
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

const messages = defineMessages({
  services: {
    id: 'Services',
    defaultMessage: 'Services',
  },
});

export const ServicesInfo = ({ content, className }: ServicesInfoProps) => {
  const intl = useIntl();
  const classes = ['services-info'];
  if (className) classes.push(className);
  const services = content?.services || [];

  return (
    services.length > 0 && (
      <Container className={classes.join(' ')}>
        <h2 className="blockTitle servicesTitle">
          {intl.formatMessage(messages.services)}
        </h2>
        <ul className="servicesWrapper">
          {services.map((service, index) => (
            <li key={index} className={`service-item ${service.token}`}>
              {service.title}
            </li>
          ))}
        </ul>
      </Container>
    )
  );
};

export default ServicesInfo;
