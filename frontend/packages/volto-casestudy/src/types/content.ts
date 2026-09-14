import type { Content, Image, RelatedItem } from '@plone/types';
import type { WorkflowStateValue } from '@plone-collective/volto-multiworkflow';

/**
 * `@plone/types` declares `Content['subjects']` as the empty tuple `[]`, which
 * no real payload satisfies. Both content types re-declare it as `string[]`.
 */
type ContentBase = Omit<Content, 'subjects'>;

/** A term coming from a `zope.schema.Choice` / `List` serialized by plone.restapi. */
export interface VocabularyTerm {
  token: string;
  title?: string;
}

/**
 * One entry of the `social_links` field, provided by the
 * `plonegovbr.socialmedia.links` behavior.
 *
 * `id` is a social network id registered as a `socialNetwork` utility by
 * `@plonegovbr/volto-social-media` — `website`, `mastodon`, `github`, …
 */
export interface SocialMediaItem {
  '@id': string;
  href: {
    '@id': string;
    title: string;
  }[];
  id: string;
  title: string;
}

/**
 * `image_scales` as serialized on a summary: a mapping of field name to a
 * *list* of images.
 *
 * `@plone/types` types `RelatedItem['image_scales']` as `Record<string, Image>`,
 * but plone.restapi emits `{ image: [ … ] }` — an array per field.
 */
export interface ImageScalesSummary {
  [key: string]: Image[];
}

/**
 * A catalog summary, as serialized for a relation value or a listing entry.
 *
 * `@plone/types` types `RelatedItem['image_scales']` as `Record<string, Image>`,
 * so it is re-declared here as `ImageScalesSummary`.
 */
export interface ContentSummary extends Omit<RelatedItem, 'image_scales'> {
  image_scales: ImageScalesSummary | null;
}

/**
 * The `preview_image_link` relation, provided by the
 * `volto.preview_image_link` behavior.
 *
 * The `download` path inside `image_scales` is relative to this item's `@id`.
 */
export type PreviewImageLink = ContentSummary;

/**
 * An `Organization` as it appears in the `organizations` / `providers`
 * relation lists of a `CaseStudy`.
 *
 * `image_field` is `preview_image_link` whenever the organization has a logo,
 * and the matching `image_scales` entry then carries a `base_path` pointing at
 * the linked image — its `download` paths are relative to *that*, not to the
 * organization. `@plone/volto`'s `Image` component resolves both cases.
 */
export type OrganizationSummary = ContentSummary;

/**
 * A `CaseStudy` as it appears inside an organization's `case_studies`.
 *
 * `ContentSummary` rather than `RelatedItem`: rendering the screenshot means
 * reading `image_scales`, which `@plone/types` mistypes as one image per
 * field where plone.restapi emits a list.
 */
export type CaseStudySummary = ContentSummary;

/**
 * The case studies an organization takes part in, as the backend serializer
 * reports them: `provided` are the ones it delivered as a solution provider,
 * `received` the ones it is the subject of.
 */
export interface CaseStudyRelations {
  provided: CaseStudySummary[];
  received: CaseStudySummary[];
}

export interface CaseStudy extends ContentBase {
  title: string;
  description: string;
  remoteUrl: string;
  preview_image_link: PreviewImageLink | null;
  preview_caption_link: string | null;
  industry: VocabularyTerm | null;
  usages: VocabularyTerm[];
  versions: VocabularyTerm[];
  organizations: OrganizationSummary[];
  providers: OrganizationSummary[];
  subjects: string[];
}

export interface Organization extends ContentBase {
  title: string;
  description: string;
  preview_image_link: PreviewImageLink | null;
  preview_caption_link: string | null;
  organization_size: VocabularyTerm | null;
  social_links: SocialMediaItem[];
  // collective.casestudy.contact_info
  contact_name: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  // collective.casestudy.address_info
  address: string | null;
  address_2: string | null;
  city: string | null;
  state: string | null;
  postal_code: string | null;
  country: VocabularyTerm | null;
  // collective.casestudy.provider_info
  is_provider: boolean;
  services: VocabularyTerm[];
  subjects: string[];
  case_studies: CaseStudyRelations;
  /**
   * The state in every workflow of the chain, as `<workflow-id>|<state-id>`,
   * primary workflow first. Read it with the helpers of
   * `@plone-collective/volto-multiworkflow`.
   */
  workflow_states: WorkflowStateValue[];
}
