import React from 'react';
import cx from 'classnames';
import OrganizationLink from '@plone-collective/volto-casestudy/components/OrganizationLink/OrganizationLink';
import type { OrganizationSummary } from '@plone-collective/volto-casestudy/types/content';
import './organization-list.scss';

export interface OrganizationListProps {
  items: OrganizationSummary[];
  /** Extra classes for the wrapper. */
  className?: string;
}

/** Related organizations as a wrapping row of links, logo first. */
export const OrganizationList = ({
  items,
  className,
}: OrganizationListProps) => (
  <div className={cx('organization-list', className)}>
    {items.map((item) => (
      <OrganizationLink key={item['@id']} item={item} showLogo />
    ))}
  </div>
);

export default OrganizationList;
