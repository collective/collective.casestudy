import React from 'react';
import { Container } from '@plone/components';
import SlotRenderer from '@plone/volto/components/theme/SlotRenderer/SlotRenderer';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import OrganizationHeader from '@plone-collective/volto-casestudy/components/OrganizationHeader/OrganizationHeader';
import OrganizationInfo from '@plone-collective/volto-casestudy/components/OrganizationInfo/OrganizationInfo';
import { ORGANIZATION_FOOTER_SLOT } from '@plone-collective/volto-casestudy/config/slots';
import './organization.scss';

/**
 * `SlotRenderer` typed by what it actually needs.
 *
 * Its props extend `GetSlotArgs`, which requires `location` and a
 * `@plone/types` `Content`. Neither holds in practice: the component reads
 * the location from the router itself, and `Content['subjects']` is declared
 * as the empty tuple `[]`, which no real payload satisfies -- the same
 * upstream mismatch `types/content.ts` works around with `Omit`. Every call
 * site in Volto passes just `name` and `content`, and all but one are `.jsx`,
 * where the prop type is never checked.
 */
const Slot = SlotRenderer as unknown as React.FC<{
  name: string;
  content: Organization;
}>;

interface OrganizationViewProps {
  /** The organization, as the backend serializes it. */
  content: Organization;
  /** Everything else Volto passes to a view. */
  [key: string]: any;
}

/**
 * Page of an organization: logo, title, description, social links and the
 * case studies it takes part in.
 *
 * Registered as the content type view of `Organization`. A provider whose
 * listing is public is reported by the backend with the `providerView` layout
 * and rendered by `ProviderView` instead, so this page never shows provider
 * information.
 *
 * The case studies come from the organization footer slot rather than from a
 * call here: whether there are any to show is the `hasCaseStudies` predicate's
 * decision, and a site can register more components into the same slot.
 */
const OrganizationView: React.FC<OrganizationViewProps> = ({ content }) => {
  return (
    <Container id="page-document" className="view-wrapper organization-view">
      <Container className="mainWrapper ui container">
        <OrganizationHeader content={content} isVerified={false} label="" />
        <OrganizationInfo content={content} />
      </Container>
      <Slot name={ORGANIZATION_FOOTER_SLOT} content={content} />
    </Container>
  );
};

export default OrganizationView;
