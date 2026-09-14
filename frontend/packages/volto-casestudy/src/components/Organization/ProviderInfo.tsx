import React from 'react';
import { Container } from '@plone/components';
import {
  formatWorkflowState,
  getWorkflowStates,
} from '@plone-collective/volto-multiworkflow';
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

/** The `workflow_states` value of a verified provider. */
const VERIFIED = formatWorkflowState('provider_workflow', 'verified');

export const ProviderInfo = ({ content, className }: ProviderInfoProps) => {
  const classes = ['provider-info'];
  const isVerified = getWorkflowStates(content).includes(VERIFIED);
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
