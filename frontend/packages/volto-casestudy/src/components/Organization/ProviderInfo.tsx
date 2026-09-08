import React from 'react';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import AddressInfo from './AddressInfo';
import ServicesList from './ServicesList';
import VerifiedBadge from './VerifiedBadge';
import './provider-info.scss';

export interface ProviderInfoProps {
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

export const ProviderInfo = ({ content, className }: ProviderInfoProps) => {
  const classes = ['provider-info'];
  const workflow_states = content?.workflow_states || {};
  const isVerified =
    workflow_states?.['provider_workflow'] === 'verified' || false;
  const services = content?.services || [];
  if (className) classes.push(className);

  return (
    <Container className={classes.join(' ')}>
      {isVerified && <VerifiedBadge className="providerBadge" />}
      <Container className="providerInfoBlocks">
        <AddressInfo content={content} className="providerInfoBlock" />
        {services.length > 0 && (
          <ServicesList content={content} className="providerInfoBlock" />
        )}
      </Container>
    </Container>
  );
};

export default ProviderInfo;
