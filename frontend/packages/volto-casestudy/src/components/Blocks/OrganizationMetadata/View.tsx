import React from 'react';
import { Header, List, Segment } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';
import { getWebsiteUrl } from '@plone-collective/volto-casestudy/helpers/socialLinks';
import { useMetadataContent } from '@plone-collective/volto-casestudy/hooks/useMetadataContent';
import { PreviewImage } from '../CaseStudyMetadata/View';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import type { OrganizationMetadataData } from './index';
import './organization-metadata.scss';

const messages = defineMessages({
  contact_person: {
    id: 'provider_contact_person',
    defaultMessage: 'Contact Person',
  },
  contact_email: {
    id: 'provider_contact_email',
    defaultMessage: 'Contact Email',
  },
  contact_phone_number: {
    id: 'provider_contact_phone_number',
    defaultMessage: 'Contact Phone Number',
  },
  country: { id: 'provider_country', defaultMessage: 'Country' },
  organization_size: {
    id: 'provider_organization_size',
    defaultMessage: 'Organization Size',
  },
  what: { id: 'organization_what', defaultMessage: 'What' },
  website: { id: 'website', defaultMessage: 'Website' },
  visitWebsite: {
    id: 'visit_external_website',
    defaultMessage: 'Visit external website',
  },
});

export interface OrganizationMetadataViewProps {
  data: OrganizationMetadataData;
  properties?: Organization;
}

export const OrganizationMetadataView = ({
  data,
  properties,
}: OrganizationMetadataViewProps) => {
  const intl = useIntl();
  const targetPath = data?.organization_source?.[0]?.['@id'];
  const content = useMetadataContent<Organization>(targetPath, properties);

  if (!content) return null;

  // Organization has no `remoteUrl`; the company site is a `website` entry
  // in the `social_links` field.
  const websiteUrl = getWebsiteUrl(content.social_links);

  return (
    <Segment as="aside" floated="right" className="organization-metadata-block">
      {content.preview_image_link && (
        <>
          <div className="company-logo">
            <PreviewImage
              link={content.preview_image_link}
              caption={content.preview_caption_link}
            />
          </div>
        </>
      )}

      {content.contact_name && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.contact_person)}
          </Header>
          <p>{content.contact_name}</p>
        </>
      )}

      {content.contact_email && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.contact_email)}
          </Header>
          <p>{content.contact_email}</p>
        </>
      )}

      {content.contact_phone && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.contact_phone_number)}
          </Header>
          <p>{content.contact_phone}</p>
        </>
      )}

      {content.country?.title && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.country)}
          </Header>
          <p>{content.country.title}</p>
        </>
      )}

      {content.organization_size?.title && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.organization_size)}
          </Header>
          <p>{content.organization_size.title}</p>
        </>
      )}

      {websiteUrl && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.website)}
          </Header>
          <p>
            <a href={websiteUrl} target="_blank" rel="noopener noreferrer">
              {intl.formatMessage(messages.visitWebsite)}
            </a>
          </p>
        </>
      )}

      {content.subjects?.length > 0 && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.what)}
          </Header>
          <List items={content.subjects} />
        </>
      )}
    </Segment>
  );
};

export default OrganizationMetadataView;
