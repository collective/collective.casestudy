import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { Header, List, Segment } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';

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
  screenshot: { id: 'provider_screenshot', defaultMessage: 'Screenshot' },
  website: { id: 'website', defaultMessage: 'Website' },
  visitWebsite: {
    id: 'visit_external_website',
    defaultMessage: 'Visit external website',
  },
});

const PreviewImage = ({ content }: { content: any }) => {
  const { preview_image, preview_caption } = content;
  const scale_name = 'preview';
  if (!preview_image?.scales?.[scale_name]) return null;
  const scale = preview_image.scales[scale_name];
  const { download, height, width } = scale;

  return (
    <img
      src={download}
      alt={preview_caption || ''}
      height={height}
      width={width}
      style={{ maxWidth: '100%', height: 'auto', display: 'block' }}
    />
  );
};

interface ViewProps {
  data: any;
  properties: any;
}

const ProviderMetadataView = ({ data, properties }: ViewProps) => {
  const intl = useIntl();
  const [externalContent, setExternalContent] = useState<any>(null);
  const [isClient, setIsClient] = useState(false);

  const targetPath = data?.provider_source?.[0]?.['@id'];

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (!isClient || !targetPath) {
      setExternalContent(null);
      return;
    }

    const relativePath = targetPath.replace(/^https?:\/\/[^/]+/, '');
    const targetUrl = `${window.location.origin}/++api++${relativePath}`;

    fetch(targetUrl, { headers: { Accept: 'application/json' } })
      .then((res) => (res.ok ? res.json() : null))
      .then((jsonData) => {
        if (jsonData) setExternalContent(jsonData);
      })
      .catch(() => {});
  }, [targetPath, isClient]);

  const content = targetPath ? externalContent : properties;

  if (!isClient || !content) return null;

  return (
    <Segment
      as="aside"
      floated="right"
      className="provider-metadata-block-view"
      style={{
        display: 'inline-block',
        width: 'max-content',
        maxWidth: '450px',
        marginLeft: '2em',
        marginBottom: '1em',
        marginTop: '0',
      }}
    >
      {content.preview_image && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.screenshot)}
          </Header>
          <div className="website-image">
            <PreviewImage content={content} />
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

      {content.remoteUrl && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.website)}
          </Header>
          <p>
            <a
              href={content.remoteUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
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

ProviderMetadataView.propTypes = {
  data: PropTypes.object.isRequired,
  properties: PropTypes.object.isRequired,
};

export default ProviderMetadataView;
