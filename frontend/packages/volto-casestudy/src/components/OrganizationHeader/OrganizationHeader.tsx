import React from 'react';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import OrganizationLogo from '@plone-collective/volto-casestudy/components/OrganizationLogo/OrganizationLogo';
import OrganizationSocialLinks from '@plone-collective/volto-casestudy/components/OrganizationSocialLinks/OrganizationSocialLinks';
import VerifiedBadge from '@plone-collective/volto-casestudy/components/VerifiedBadge/VerifiedBadge';
import './organization-header.scss';

interface OrganizationHeaderProps {
  /** The organization, as the backend serializes it. */
  content: Organization;
  label: string;
  isVerified: boolean;
  /** Everything else Volto passes to a view. */
  [key: string]: any;
}

const OrganizationHeader: React.FC<OrganizationHeaderProps> = ({
  content,
  label,
  isVerified = false,
}) => {
  return (
    <Container className="organizationHeader">
      <OrganizationLogo content={content} align="center" size="large" />
      <Container className="organizationSummary">
        <span className="organizationLabel">{label}</span>
        <h1 className="organizationTitle">
          {content.title}{' '}
          {isVerified && <VerifiedBadge className="verifiedBadge" />}
        </h1>
        <p className="organizationDescription">{content.description}</p>
        <OrganizationSocialLinks content={content} align="left" size="medium" />
      </Container>
    </Container>
  );
};

export default OrganizationHeader;
