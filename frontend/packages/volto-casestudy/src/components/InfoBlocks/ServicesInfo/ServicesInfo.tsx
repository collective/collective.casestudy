import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import InfoBox from '@plone-collective/volto-casestudy/components/InfoBlocks/InfoBox/InfoBox';
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
  const services = content?.services || [];
  if (services.length === 0) return null;

  return (
    <InfoBox
      name="services"
      title={intl.formatMessage(messages.services)}
      as="ul"
      className={className}
    >
      {services.map((service, index) => (
        <li key={index} className={`service-item ${service.token}`}>
          {service.title}
        </li>
      ))}
    </InfoBox>
  );
};

export default ServicesInfo;
