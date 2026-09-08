import React from 'react';
import { Container } from '@plone/components';
import Image from '@plone/volto/components/theme/Image/Image';
import SocialNetworks from '@plonegovbr/volto-social-media/components/SocialNetworks/SocialNetworks';
import type {
  Organization,
  PreviewImageLink,
} from '@plone-collective/volto-casestudy/types/content';
import CaseStudies from '@plone-collective/volto-casestudy/components/Organization/CaseStudies';
import ProviderInfo from '@plone-collective/volto-casestudy/components/Organization/ProviderInfo';
import './organization.scss';

interface OrganizationViewProps {
  content: Organization;
  [key: string]: any;
}

interface OrganizationLogoProps {
  previewImage: PreviewImageLink | null;
  previewImageAlt: string | null;
}

const OrganizationLogo: React.FC<OrganizationLogoProps> = ({
  previewImage,
  previewImageAlt,
}) => {
  if (!previewImage) {
    return null;
  }
  return (
    <div className="organizationLogo">
      <figure className="figure right medium">
        <Image
          item={previewImage}
          alt={previewImageAlt || previewImage?.title}
          loading="lazy"
          responsive={true}
        />
      </figure>
    </div>
  );
};

const OrganizationView: React.FC<OrganizationViewProps> = ({ content }) => {
  const previewImage = content?.preview_image_link;
  const previewImageAlt = content?.preview_caption_link;
  const social_links = content?.social_links || [];
  const case_studies = content?.case_studies;
  const isProvider = content?.is_provider || false;
  const hasCaseStudies =
    case_studies?.provided?.length > 0 || case_studies?.received?.length > 0;
  return (
    <Container
      id="page-document"
      className="view-wrapper ui container organization-view"
    >
      <OrganizationLogo
        previewImage={previewImage}
        previewImageAlt={previewImageAlt}
      />
      <h1 className="documentFirstHeading">{content.title}</h1>
      <p className="description">{content.description}</p>
      <Container className="socialNetworks">
        <SocialNetworks networks={social_links} />
      </Container>
      {isProvider && (
        <ProviderInfo content={content} className="organizationInfoBlock" />
      )}
      {hasCaseStudies && (
        <Container className="caseStudies organizationInfoBlock">
          <CaseStudies case_studies={case_studies} />
        </Container>
      )}
    </Container>
  );
};

export default OrganizationView;
