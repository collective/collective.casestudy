import React from 'react';
import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';
import type { CaseStudy } from '@plone-collective/volto-casestudy/types/content';
import { Message, Icon } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';
import CaseStudyMetadataDataForm from './Data';
import CaseStudyMetadataView from './View';
import type { CaseStudyMetadataData } from './index';

const messages = defineMessages({
  blockName: {
    id: 'Case Study Metadata Block',
    defaultMessage: 'Case Study Metadata Block',
  },
  source: { id: 'Source', defaultMessage: 'Source' },
  customSelection: {
    id: 'Custom page selection',
    defaultMessage: 'Custom page selection',
  },
  currentContext: {
    id: 'Current context page properties',
    defaultMessage: 'Current context page properties',
  },
});

export interface CaseStudyMetadataEditProps {
  data: CaseStudyMetadataData;
  block: string;
  selected: boolean;
  properties?: CaseStudy;
  content?: CaseStudy;
  onChangeBlock: (id: string, data: CaseStudyMetadataData) => void;
}

const CaseStudyMetadataEdit: React.FC<CaseStudyMetadataEditProps> = (props) => {
  const { block, data, onChangeBlock, selected, content, properties } = props;
  const intl = useIntl();
  const targetPath = data?.case_study_source?.[0]?.['@id'];
  const objectData = content ?? properties;
  const showView =
    objectData && objectData['@type'] === 'CaseStudy' && objectData?.id;
  return (
    <>
      {showView ? (
        <CaseStudyMetadataView data={data} properties={objectData} />
      ) : (
        <div className="case-study-block-edit">
          <Message icon info>
            <Icon name="info circle" />
            <Message.Content>
              <Message.Header>
                {intl.formatMessage(messages.blockName)}
              </Message.Header>
              {targetPath ? (
                <p>
                  <strong>{intl.formatMessage(messages.source)}:</strong>{' '}
                  {intl.formatMessage(messages.customSelection)} (
                  <code>{targetPath}</code>)
                </p>
              ) : (
                <p>
                  <strong>{intl.formatMessage(messages.source)}:</strong>{' '}
                  {intl.formatMessage(messages.currentContext)}
                </p>
              )}
            </Message.Content>
          </Message>
        </div>
      )}
      <SidebarPortal selected={selected}>
        <CaseStudyMetadataDataForm
          data={data}
          block={block}
          onChangeBlock={onChangeBlock}
        />
      </SidebarPortal>
    </>
  );
};

export default CaseStudyMetadataEdit;
