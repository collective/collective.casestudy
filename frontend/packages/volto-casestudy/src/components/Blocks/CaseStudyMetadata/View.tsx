import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { Header, List, Segment } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';

const messages = defineMessages({
  industry: { id: 'case_study_industry', defaultMessage: 'Industry' },
  usage: { id: 'case_study_usage', defaultMessage: 'Usage' },
  versions: { id: 'case_study_versions', defaultMessage: 'Versions' },
  screenshot: { id: 'case_study_screenshot', defaultMessage: 'Screenshot' },
  what: { id: 'case_study_what', defaultMessage: 'What' },
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

const CaseStudyMetadataView = ({ data, properties }: ViewProps) => {
  const intl = useIntl();
  const [externalContent, setExternalContent] = useState<any>(null);
  const [isClient, setIsClient] = useState(false);

  const targetPath = data?.case_study_source?.[0]?.['@id'];

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
      className="case-study-block-view"
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

      {content.industry?.title && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.industry)}
          </Header>
          <p>{content.industry.title}</p>
        </>
      )}

      {content.usages?.length > 0 && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.usage)}
          </Header>
          <p>
            {content.usages.map((v: any, index: number) => (
              <span key={v.token || index}>
                {v.title}
                {index < content.usages.length - 1 ? ', ' : ''}
              </span>
            ))}
          </p>
        </>
      )}

      {content.versions?.length > 0 && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.versions)}
          </Header>
          <p>
            {content.versions.map((v: any, index: number) => (
              <span key={v.token || index}>
                {v.title}
                {index < content.versions.length - 1 ? ', ' : ''}
              </span>
            ))}
          </p>
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

CaseStudyMetadataView.propTypes = {
  data: PropTypes.object.isRequired,
  properties: PropTypes.object.isRequired,
};

export default CaseStudyMetadataView;
