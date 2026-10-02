import React from 'react';
import cx from 'classnames';
import { List } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';
import { useMetadataContent } from '@plone-collective/volto-casestudy/hooks/useMetadataContent';
import InfoBox from '@plone-collective/volto-casestudy/components/InfoBlocks/InfoBox/InfoBox';
import IndustryInfo from '@plone-collective/volto-casestudy/components/InfoBlocks/IndustryInfo/IndustryInfo';
import OrganizationList from '@plone-collective/volto-casestudy/components/OrganizationList/OrganizationList';
import PreviewImage from '@plone-collective/volto-casestudy/components/PreviewImage/PreviewImage';
import TermList from '@plone-collective/volto-casestudy/components/TermList/TermList';
import type { CaseStudy } from '@plone-collective/volto-casestudy/types/content';
import type { CaseStudyMetadataData } from './index';
import { LAYOUT_IMAGE_SCALE, resolveLayout } from './layout';
import './casestudy-metadata.scss';

const messages = defineMessages({
  usage: { id: 'case_study_usage', defaultMessage: 'Usage' },
  versions: { id: 'case_study_versions', defaultMessage: 'Versions' },
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

/** Class every section of the block carries, whatever its kind. */
const BOX = 'metadata-box';

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
  const layout = resolveLayout(data?.layout);

  if (!content) return null;

  return (
    <aside
      className={cx('casestudy-metadata-block', `layout-${layout}`, {
        'ui segment right floated': layout === 'compact',
      })}
    >
      {content.preview_image_link && (
        <figure className="website-image">
          <PreviewImage
            link={content.preview_image_link}
            caption={content.preview_caption_link}
            scale={LAYOUT_IMAGE_SCALE[layout]}
          />
        </figure>
      )}

      <div className="metadata-boxes">
        {content.organizations?.length > 0 && (
          <InfoBox
            name="organizations"
            title={intl.formatMessage(messages.organizations)}
            as="div"
            className={BOX}
          >
            <OrganizationList items={content.organizations} />
          </InfoBox>
        )}

        {content.providers?.length > 0 && (
          <InfoBox
            name="providers"
            title={intl.formatMessage(messages.providers)}
            as="div"
            className={BOX}
          >
            <OrganizationList items={content.providers} />
          </InfoBox>
        )}

        <IndustryInfo content={content} className={BOX} />

        {content.usages?.length > 0 && (
          <InfoBox
            name="usages"
            title={intl.formatMessage(messages.usage)}
            className={BOX}
          >
            <TermList terms={content.usages} />
          </InfoBox>
        )}

        {content.versions?.length > 0 && (
          <InfoBox
            name="versions"
            title={intl.formatMessage(messages.versions)}
            className={BOX}
          >
            <TermList terms={content.versions} />
          </InfoBox>
        )}

        {content.remoteUrl && (
          <InfoBox
            name="website"
            title={intl.formatMessage(messages.website)}
            className={BOX}
          >
            <a
              href={content.remoteUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              {intl.formatMessage(messages.visitWebsite)}
            </a>
          </InfoBox>
        )}

        {content.subjects?.length > 0 && (
          <InfoBox
            name="subjects"
            title={intl.formatMessage(messages.what)}
            as="div"
            className={BOX}
          >
            <List items={content.subjects} />
          </InfoBox>
        )}
      </div>
    </aside>
  );
};

export default CaseStudyMetadataView;
