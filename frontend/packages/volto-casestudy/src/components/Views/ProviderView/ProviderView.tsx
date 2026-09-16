import React from 'react';
import { defineMessages, useIntl } from 'react-intl';
import { Container } from '@plone/components';
import SlotRenderer from '@plone/volto/components/theme/SlotRenderer/SlotRenderer';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';
import OrganizationHeader from '@plone-collective/volto-casestudy/components/OrganizationHeader/OrganizationHeader';
import ProviderInfo from '@plone-collective/volto-casestudy/components/ProviderInfo/ProviderInfo';
import { ORGANIZATION_FOOTER_SLOT } from '@plone-collective/volto-casestudy/config/slots';
import {
  formatWorkflowState,
  getWorkflowStates,
} from '@plone-collective/volto-multiworkflow';
import './provider.scss';

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

interface ProviderViewProps {
  /** The organization, as the backend serializes it. */
  content: Organization;
  /** Everything else Volto passes to a view. */
  [key: string]: any;
}
/** The `workflow_states` value of a verified provider. */
const VERIFIED = formatWorkflowState('provider_workflow', 'verified');

const messages = defineMessages({
  provider: {
    id: 'Provider',
    defaultMessage: 'Provider',
  },
  about: {
    id: 'About',
    defaultMessage: 'About',
  },
});

/**
 * Page of an organization that is a solution provider with a public listing.
 *
 * Registered as the `providerView` layout view. The backend reports that
 * layout for an organization flagged as a provider whose `provider_workflow`
 * state is `listed` or `verified`, and Volto resolves a layout view before the
 * content type view — so these organizations get this page instead of
 * `OrganizationView`.
 *
 * On top of what `OrganizationView` shows — logo, title, description, social
 * links and case studies — it renders the provider information: address,
 * services and, for a verified provider, the verified badge.
 *
 * The case studies come from the organization footer slot rather than from a
 * call here: whether there are any to show is the `hasCaseStudies` predicate's
 * decision, and a site can register more components into the same slot.
 */
const ProviderView: React.FC<ProviderViewProps> = ({ content }) => {
  const intl = useIntl();
  const isVerified = getWorkflowStates(content).includes(VERIFIED);
  return (
    <>
      <Container id="page-document" className="view-wrapper provider-view">
        <Container className="mainWrapper ui container">
          <OrganizationHeader
            content={content}
            label={intl.formatMessage(messages.provider)}
            isVerified={isVerified}
          />

          <ProviderInfo content={content} className="organizationInfoBlock" />
          {content.text && (
            <Container className="providerAboutSection">
              <h2 className="providerAbout">
                {intl.formatMessage(messages.about)}
              </h2>
              <div
                className="text"
                dangerouslySetInnerHTML={{ __html: content.text.data }}
              />
            </Container>
          )}
        </Container>
        <Slot name={ORGANIZATION_FOOTER_SLOT} content={content} />
      </Container>
    </>
  );
};

export default ProviderView;
