import React from 'react';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import AddressInfo from '@plone-collective/volto-casestudy/components/InfoBlocks/AddressInfo/AddressInfo';
import IndustryInfo from '@plone-collective/volto-casestudy/components/InfoBlocks/IndustryInfo/IndustryInfo';
import './organization-info.scss';

export interface OrganizationInfoProps {
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

export const OrganizationInfo = ({
  content,
  className,
}: OrganizationInfoProps) => {
  const classes = ['organization-info'];
  if (className) classes.push(className);

  return (
    <Container className={classes.join(' ')}>
      <Container className="organizationInfoBlocks">
        <AddressInfo content={content} className="organizationInfoBlock" />
        <IndustryInfo content={content} className="organizationInfoBlock" />
      </Container>
    </Container>
  );
};

export default OrganizationInfo;
