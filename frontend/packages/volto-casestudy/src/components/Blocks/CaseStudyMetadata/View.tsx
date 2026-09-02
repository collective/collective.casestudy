import React from 'react';
import { Header, List, Segment } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';
import { getPreviewImageSource } from '@plone-collective/volto-casestudy/helpers/preview';
import { useMetadataContent } from '@plone-collective/volto-casestudy/hooks/useMetadataContent';
import OrganizationLink from '@plone-collective/volto-casestudy/components/Organization/OrganizationLink';
import type {
  CaseStudy,
  OrganizationSummary,
  PreviewImageLink,
  VocabularyTerm,
} from '@plone-collective/volto-casestudy/types/content';
import type { CaseStudyMetadataData } from './index';
import './casestudy-metadata.scss';

const messages = defineMessages({
  industry: { id: 'case_study_industry', defaultMessage: 'Industry' },
  usage: { id: 'case_study_usage', defaultMessage: 'Usage' },
  versions: { id: 'case_study_versions', defaultMessage: 'Versions' },
  screenshot: { id: 'case_study_screenshot', defaultMessage: 'Screenshot' },
  what: { id: 'case_study_what', defaultMessage: 'What' },
  organizations: {
    id: 'case_study_organizations',
    defaultMessage: 'Organizations',
  },
  providers: { id: 'case_study_providers', defaultMessage: 'Providers' },
  website: { id: 'website', defaultMessage: 'Website' },
  visitWebsite: {
    id: 'visit_external_website',
    defaultMessage: 'Visit external website',
  },
});

interface PreviewImageProps {
  link: PreviewImageLink | null;
  caption: string | null;
}

export const PreviewImage: React.FC<PreviewImageProps> = ({
  link,
  caption,
}) => {
  const source = getPreviewImageSource(link);
  if (!source) return null;

  return (
    <img
      src={source.src}
      alt={caption || ''}
      height={source.height}
      width={source.width}
      className="preview-image"
    />
  );
};

/** Render a list of vocabulary terms as a comma-separated line. */
const TermList: React.FC<{ terms: VocabularyTerm[] }> = ({ terms }) => (
  <p>
    {terms.map((term, index) => (
      <span key={term.token || index}>
        {term.title}
        {index < terms.length - 1 ? ', ' : ''}
      </span>
    ))}
  </p>
);

/** Render related organizations as a list of links, logo first. */
const OrganizationList: React.FC<{ items: OrganizationSummary[] }> = ({
  items,
}) => (
  <div className="organization-list">
    {items.map((item) => (
      <OrganizationLink key={item['@id']} item={item} showLogo />
    ))}
  </div>
);

export interface CaseStudyMetadataViewProps {
  data: CaseStudyMetadataData;
  properties?: CaseStudy;
}

export const CaseStudyMetadataView = ({
  data,
  properties,
}: CaseStudyMetadataViewProps) => {
  const intl = useIntl();
  const targetPath = data?.case_study_source?.[0]?.['@id'];
  const content = useMetadataContent<CaseStudy>(targetPath, properties);

  if (!content) return null;

  return (
    <Segment as="aside" floated="right" className="casestudy-metadata-block">
      {content.preview_image_link && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.screenshot)}
          </Header>
          <div className="website-image">
            <PreviewImage
              link={content.preview_image_link}
              caption={content.preview_caption_link}
            />
          </div>
        </>
      )}

      {content.organizations?.length > 0 && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.organizations)}
          </Header>
          <OrganizationList items={content.organizations} />
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
          <TermList terms={content.usages} />
        </>
      )}

      {content.versions?.length > 0 && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.versions)}
          </Header>
          <TermList terms={content.versions} />
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

      {content.providers?.length > 0 && (
        <>
          <Header dividing sub>
            {intl.formatMessage(messages.providers)}
          </Header>
          <OrganizationList items={content.providers} />
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

export default CaseStudyMetadataView;
