import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import { Container } from '@plone/components';
import UniversalLink from '@plone/volto/components/manage/UniversalLink/UniversalLink';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './contact-info.scss';

export interface ContactInfoProps {
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

const messages = defineMessages({
  contact: {
    id: 'Contact',
    defaultMessage: 'Contact',
  },
});

export const ContactInfo = ({ content, className }: ContactInfoProps) => {
  const intl = useIntl();
  const classes = ['contact-info'];
  if (className) classes.push(className);

  const contact_name = content?.contact_name || '';
  const contact_email = content?.contact_email || '';
  const contact_phone = content?.contact_phone || '';
  const display = contact_name || contact_email || contact_phone;

  return (
    display && (
      <Container className={classes.join(' ')}>
        <h2 className="blockTitle contactTitle">
          {intl.formatMessage(messages.contact)}
        </h2>
        <p className="contactWrapper">
          {contact_name && (
            <span className="contactLine contactName">{contact_name}</span>
          )}
          {contact_email && (
            <span className="contactLine contactEmail">
              <UniversalLink href={`mailto:${contact_email}`}>
                {contact_email}
              </UniversalLink>
            </span>
          )}
          {contact_phone && (
            <span className="contactLine contactPhone">{contact_phone}</span>
          )}
        </p>
      </Container>
    )
  );
};

export default ContactInfo;
