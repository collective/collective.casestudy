import React from 'react';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import CaseStudies from '@plone-collective/volto-casestudy/components/Organization/CaseStudies';
import OrganizationLogo from '@plone-collective/volto-casestudy/components/Organization/OrganizationLogo';
import OrganizationSocialLinks from '@plone-collective/volto-casestudy/components/Organization/OrganizationSocialLinks';
import ProviderInfo from '@plone-collective/volto-casestudy/components/Organization/ProviderInfo';
import './provider.scss';

interface ProviderViewProps {
  /** The organization, as the backend serializes it. */
  content: Organization;
  /** Everything else Volto passes to a view. */
  [key: string]: any;
}

/**
 * Page of an organization that is a solution provider with a public listing.
 *
 * Registered as the `providerView` layout view. The backend reports that
 * layout for an organization flagged as a provider whose `provider_workflow`
 * state is `listed` or `verified`, and Volto resolves a layout view before the
 * content type view — so these organizations get this page instead of
 * `OrganizationView`.
 *
 * On top of what `OrganizationView` shows — logo, title, description, social
 * links and case studies — it renders the provider information: address,
 * services and, for a verified provider, the verified badge.
 */
const ProviderView: React.FC<ProviderViewProps> = ({ content }) => {
  const case_studies = content?.case_studies;
  const hasCaseStudies =
    case_studies?.provided?.length > 0 || case_studies?.received?.length > 0;
  return (
    <Container
      id="page-document"
      className="view-wrapper ui container provider-view"
    >
      <OrganizationLogo content={content} />
      <h1 className="documentFirstHeading">{content.title}</h1>
      <p className="description">{content.description}</p>
      <OrganizationSocialLinks content={content} />
      <ProviderInfo content={content} className="organizationInfoBlock" />
      {hasCaseStudies && (
        <Container className="caseStudies organizationInfoBlock">
          <CaseStudies case_studies={case_studies} />
        </Container>
      )}
    </Container>
  );
};

export default ProviderView;
