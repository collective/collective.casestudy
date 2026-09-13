import React from 'react';
import { Container } from '@plone/components';
import SocialNetworks from '@plonegovbr/volto-social-media/components/SocialNetworks/SocialNetworks';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './organization-social-links.scss';

export interface OrganizationSocialLinksProps {
  /** The organization whose `social_links` are rendered. */
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

/**
 * The networks an organization is on, as a row of icons.
 *
 * Renders the `social_links` field through `SocialNetworks` from
 * `@plonegovbr/volto-social-media`, which drops a link with no target. The
 * container is always rendered, even when there are no links.
 */
export const OrganizationSocialLinks = ({
  content,
  className,
}: OrganizationSocialLinksProps) => {
  const classes = ['socialNetworks'];
  if (className) classes.push(className);
  const social_links = content?.social_links || [];

  return (
    <Container className={classes.join(' ')}>
      <SocialNetworks networks={social_links} />
    </Container>
  );
};

export default OrganizationSocialLinks;
