import React from 'react';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './services-list.scss';

export interface ServicesListProps {
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

export const ServicesList = ({ content, className }: ServicesListProps) => {
  const classes = ['services-list'];
  if (className) classes.push(className);
  const services = content?.services || [];

  return (
    <Container className={classes.join(' ')}>
      <h2 className="servicesTitle">Services</h2>
      <ul className="servicesWrapper">
        {services.map((service, index) => (
          <li key={index} className={`service-item ${service.token}`}>
            {service.title}
          </li>
        ))}
      </ul>
    </Container>
  );
};

export default ServicesList;
