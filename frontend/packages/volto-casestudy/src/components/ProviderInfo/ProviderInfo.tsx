import React from 'react';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import AddressInfo from '@plone-collective/volto-casestudy/components/InfoBlocks/AddressInfo/AddressInfo';
import ContactInfo from '@plone-collective/volto-casestudy/components/InfoBlocks/ContactInfo/ContactInfo';
import ServicesInfo from '@plone-collective/volto-casestudy/components/InfoBlocks/ServicesInfo/ServicesInfo';
import './provider-info.scss';

export interface ProviderInfoProps {
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

export const ProviderInfo = ({ content, className }: ProviderInfoProps) => {
  const classes = ['provider-info'];
  if (className) classes.push(className);

  return (
    <Container className={classes.join(' ')}>
      <Container className="providerInfoBlocks">
        <AddressInfo content={content} className="providerInfoBlock" />
        <ContactInfo content={content} className="providerInfoBlock" />
        <ServicesInfo content={content} className="providerInfoBlock" />
      </Container>
    </Container>
  );
};

export default ProviderInfo;
