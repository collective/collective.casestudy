import CaseStudies from '@plone-collective/volto-casestudy/components/CaseStudies/CaseStudies';
import type { Organization } from '@plone-collective/volto-casestudy/types/content';

export interface CaseStudiesSlotProps {
  /** The organization, as the backend serializes it. */
  content: Organization;
}

/**
 * Renders an organization's case studies into the case studies slot.
 *
 * A slot component is handed the whole `content`, while `CaseStudies` takes
 * the `case_studies` value on its own. Unwrapping it here keeps that
 * component usable outside a slot instead of widening its API to suit one.
 *
 * Whether this renders at all is decided by the `hasCaseStudies` predicate it
 * is registered with, so no guard is repeated here.
 */
export const CaseStudiesSlot = ({ content }: CaseStudiesSlotProps) => (
  <CaseStudies case_studies={content?.case_studies} full />
);

export default CaseStudiesSlot;
