import React from 'react';
import Image from '@plone/volto/components/theme/Image/Image';
import UniversalLink from '@plone/volto/components/manage/UniversalLink/UniversalLink';
import {
  getSummaryImageField,
  hasSummaryImage,
} from '@plone-collective/volto-casestudy/helpers/preview';
import type { OrganizationSummary } from '@plone-collective/volto-casestudy/types/content';
import './organization-link.scss';

export interface OrganizationLinkProps {
  /** The organization, as serialized inside a relation field. */
  item: OrganizationSummary;
  /**
   * Render the organization logo instead of its title. Items with no logo
   * fall back to the title, so a mixed list never renders an empty link.
   */
  showLogo?: boolean;
  align?: 'left' | 'center' | 'right';
  size?: 'small' | 'medium' | 'large';
  /** Extra classes for the link. */
  className?: string;
}

/**
 * Link to an `Organization`, rendered either as its logo or as its title.
 *
 * Takes the relation *summary* rather than the full object, so it can be
 * dropped into any component that already holds a related item — no extra
 * request is made.
 */
export const OrganizationLink = ({
  item,
  showLogo = false,
  className,
  align,
  size,
}: OrganizationLinkProps) => {
  if (!item?.['@id']) return null;

  const withLogo = showLogo && hasSummaryImage(item);
  const classes = ['organization-link', withLogo ? 'with-logo' : 'with-title'];
  if (align) classes.push(`align-${align}`);
  if (size) classes.push(`size-${size}`);
  if (className) classes.push(className);

  return (
    <UniversalLink item={item} title={item.title} className={classes.join(' ')}>
      {withLogo ? (
        <Image
          item={item}
          imageField={getSummaryImageField(item)}
          alt={item.title}
          loading="lazy"
          responsive
          className="organization-logo"
        />
      ) : (
        item.title
      )}
    </UniversalLink>
  );
};

export default OrganizationLink;
