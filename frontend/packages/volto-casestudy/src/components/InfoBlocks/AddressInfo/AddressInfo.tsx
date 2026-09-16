import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import { Container } from '@plone/components';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './address-info.scss';

export interface AddressInfoProps {
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

const messages = defineMessages({
  address: {
    id: 'Address',
    defaultMessage: 'Address',
  },
});

export const AddressInfo = ({ content, className }: AddressInfoProps) => {
  const intl = useIntl();
  const classes = ['address-info'];
  if (className) classes.push(className);

  const address = content?.address || '';
  const address_2 = content?.address_2 || '';
  const city = content?.city || '';
  const state = content?.state || '';
  const postalCode = content?.postal_code || '';
  const country = content?.country || null;

  const display =
    address || address_2 || city || state || postalCode || country;

  return (
    display && (
      <Container className={classes.join(' ')}>
        <h2 className="blockTitle addressTitle">
          {intl.formatMessage(messages.address)}
        </h2>
        <p className="addressWrapper">
          {address && <span className="addressLine address">{address}</span>}
          {address_2 && (
            <span className="addressLine address-2">{address_2}</span>
          )}
          {city && <span className="addressInline city">{city}</span>}
          {state && <span className="addressInline state">{state}</span>}
          {postalCode && (
            <span className="addressInline postal-code">{postalCode}</span>
          )}
          {country && (
            <span className="addressLine address">
              <span className={`country ${country.token}`}>
                {country.title}
              </span>
            </span>
          )}
        </p>
      </Container>
    )
  );
};

export default AddressInfo;
