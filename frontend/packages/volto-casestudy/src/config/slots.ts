import type { ConfigType } from '@plone/registry';
import CaseStudiesSlot from '../components/CaseStudies/CaseStudiesSlot';
import type { Organization } from '../types/content';

/**
 * The slot at the foot of both organization views.
 *
 * Named for the place rather than for what fills it: the case studies are
 * only the component this add-on happens to register there, and a site can
 * add or replace components without the name turning into a lie.
 *
 * Volto creates a slot the first time something is registered for it, so this
 * name does not have to be declared anywhere else.
 */
export const ORGANIZATION_FOOTER_SLOT = 'organizationFooter';

/** The name this add-on registers its own component under, inside that slot. */
export const CASE_STUDIES_COMPONENT = 'caseStudies';

/**
 * True when the organization takes part in at least one case study.
 *
 * A slot predicate is called with the arguments `SlotRenderer` collects --
 * `content`, `location`, `navRoot` and `data` -- and every predicate of a
 * component has to be true for it to render. Keeping the condition here is
 * what lets the views drop their own `hasCaseStudies &&` guard.
 */
export function hasCaseStudies({ content }: { content?: Organization }) {
  const caseStudies = content?.case_studies;
  return (
    (caseStudies?.provided?.length ?? 0) > 0 ||
    (caseStudies?.received?.length ?? 0) > 0
  );
}

/**
 * Register the slot components of the add-on.
 *
 * :param config: the Volto configuration registry.
 * :returns: the same registry, so the installers can be chained.
 */
function installSlots(config: ConfigType) {
  config.registerSlotComponent({
    slot: ORGANIZATION_FOOTER_SLOT,
    name: CASE_STUDIES_COMPONENT,
    component: CaseStudiesSlot,
    predicates: [hasCaseStudies],
  });

  return config;
}

export default installSlots;
