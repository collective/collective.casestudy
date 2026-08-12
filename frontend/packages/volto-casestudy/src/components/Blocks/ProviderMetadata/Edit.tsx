import React from 'react';
import { SidebarPortal } from '@plone/volto/components';
import InlineForm from '@plone/volto/components/manage/Form/InlineForm';
import { Message, Icon } from 'semantic-ui-react';

const ProviderMetadataEdit = (props: any) => {
  const { block, data, onChangeBlock, selected } = props;

  const schema = {
    title: 'Provider Settings',
    fieldsets: [
      { id: 'default', title: 'Settings', fields: ['provider_source'] },
    ],
    properties: {
      provider_source: {
        title: 'Source Provider',
        description: 'Leave empty to pull metadata from the current page.',
        widget: 'object_browser',
        mode: 'link',
        allowExternals: false,
        maximum: 1,
      },
    },
    required: [],
  };

  const targetPath = data?.provider_source?.[0]?.['@id'];

  return (
    <>
      <div className="provider-block-edit" style={{ margin: '0.5em 0' }}>
        <Message icon info style={{ display: 'flex', alignItems: 'center' }}>
          <Icon name="info circle" />
          <Message.Content>
            <Message.Header style={{ fontSize: '1em', marginBottom: '4px' }}>
              Provider Metadata Block
            </Message.Header>
            {targetPath ? (
              <p style={{ margin: 0, opacity: 0.85 }}>
                <strong>Source:</strong> Custom page selection (
                <code>{targetPath}</code>)
              </p>
            ) : (
              <p style={{ margin: 0, opacity: 0.85 }}>
                <strong>Source:</strong> Current context page properties
              </p>
            )}
          </Message.Content>
        </Message>
      </div>

      <SidebarPortal selected={selected}>
        <InlineForm
          schema={schema}
          title={schema.title}
          onChangeField={(id: string, value: any) => {
            onChangeBlock(block, { ...data, [id]: value });
          }}
          formData={data}
        />
      </SidebarPortal>
    </>
  );
};

export default ProviderMetadataEdit;
