import React from 'react';
import Image from '@plone/volto/components/theme/Image/Image';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import './organization-logo.scss';

export interface OrganizationLogoProps {
  /** The organization whose `preview_image_link` is its logo. */
  content: Organization;
  /** Extra classes for the container. */
  className?: string;
}

/**
 * The organization's logo, floated to the right of the page title.
 *
 * The image comes from the `preview_image_link` relation and its text
 * alternative from `preview_caption_link`, falling back to the image title.
 * Renders nothing when the organization has no logo.
 */
export const OrganizationLogo = ({
  content,
  className,
}: OrganizationLogoProps) => {
  const previewImage = content?.preview_image_link;
  if (!previewImage) return null;

  const classes = ['organizationLogo'];
  if (className) classes.push(className);

  return (
    <div className={classes.join(' ')}>
      <figure className="figure right medium">
        <Image
          item={previewImage}
          alt={content?.preview_caption_link || previewImage?.title}
          loading="lazy"
          responsive={true}
        />
      </figure>
    </div>
  );
};

export default OrganizationLogo;
