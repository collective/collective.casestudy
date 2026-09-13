import React from 'react';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import CaseStudies from '@plone-collective/volto-casestudy/components/Organization/CaseStudies';
import OrganizationLogo from '@plone-collective/volto-casestudy/components/Organization/OrganizationLogo';
import OrganizationSocialLinks from '@plone-collective/volto-casestudy/components/Organization/OrganizationSocialLinks';
import './organization.scss';

interface OrganizationViewProps {
  /** The organization, as the backend serializes it. */
  content: Organization;
  /** Everything else Volto passes to a view. */
  [key: string]: any;
}

/**
 * Page of an organization: logo, title, description, social links and the
 * case studies it takes part in.
 *
 * Registered as the content type view of `Organization`. A provider whose
 * listing is public is reported by the backend with the `providerView` layout
 * and rendered by `ProviderView` instead, so this page never shows provider
 * information.
 */
const OrganizationView: React.FC<OrganizationViewProps> = ({ content }) => {
  const case_studies = content?.case_studies;
  const hasCaseStudies =
    case_studies?.provided?.length > 0 || case_studies?.received?.length > 0;
  return (
    <Container
      id="page-document"
      className="view-wrapper ui container organization-view"
    >
      <OrganizationLogo content={content} />
      <h1 className="documentFirstHeading">{content.title}</h1>
      <p className="description">{content.description}</p>
      <OrganizationSocialLinks content={content} />
      {hasCaseStudies && (
        <Container className="caseStudies organizationInfoBlock">
          <CaseStudies case_studies={case_studies} />
        </Container>
      )}
    </Container>
  );
};

export default OrganizationView;
