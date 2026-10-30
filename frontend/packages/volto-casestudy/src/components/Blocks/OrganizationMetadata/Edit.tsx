import React from 'react';
import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';
import { Message, Icon } from 'semantic-ui-react';
import { defineMessages, useIntl } from 'react-intl';
import OrganizationMetadataDataForm from './Data';
import type { OrganizationMetadataDataProps } from './Data';

const messages = defineMessages({
  blockName: {
    id: 'Organization Metadata Block',
    defaultMessage: 'Organization Metadata Block',
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

export interface OrganizationMetadataEditProps
  extends OrganizationMetadataDataProps {
  selected: boolean;
}

const OrganizationMetadataEdit: React.FC<OrganizationMetadataEditProps> = (
  props,
) => {
  const { data, selected } = props;
  const intl = useIntl();
  const targetPath = data?.organization_source?.[0]?.['@id'];

  return (
    <>
      <div className="organization-block-edit">
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

      <SidebarPortal selected={selected}>
        <OrganizationMetadataDataForm {...props} />
      </SidebarPortal>
    </>
  );
};

export default OrganizationMetadataEdit;
