import type { ConfigType } from '@plone/registry';
import VocabularyTermsWidget from '../components/Widgets/VocabularyTermsWidget';

/**
 * Name the backend asks for, through
 * `directives.widget(..., frontendOptions={"widget": ...})` on
 * `ICaseStudySettings`. Volto's `Field` resolves this before a field's own
 * `widget`, so it wins over the `json` fallback plone.restapi reports for a
 * `JSONField`.
 */
export const TERMS_WIDGET = 'vocabulary_terms';

export default function installWidgets(config: ConfigType) {
  config.widgets.widget[TERMS_WIDGET] = VocabularyTermsWidget;

  return config;
}
