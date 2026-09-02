import type { SocialMediaItem } from '@plone-collective/volto-casestudy/types/content';

/** Network id used by `@plonegovbr/volto-social-media` for a plain web site. */
export const WEBSITE_NETWORK_ID = 'website';

/**
 * Return the first `social_links` entry registered under `id`.
 *
 * @param links - The content's `social_links` value, possibly undefined.
 * @param id - A social network id, e.g. `website` or `mastodon`.
 */
export function getSocialLink(
  links: SocialMediaItem[] | undefined | null,
  id: string,
): SocialMediaItem | undefined {
  return (links ?? []).find((link) => link?.id === id);
}

/**
 * Return the target URL of a `social_links` entry.
 *
 * The `href` field is an object-browser value, so it is a list; only the
 * first entry is meaningful.
 */
export function getSocialLinkUrl(
  links: SocialMediaItem[] | undefined | null,
  id: string,
): string | undefined {
  return getSocialLink(links, id)?.href?.[0]?.['@id'];
}

/**
 * Return the organization's own web site, if one was added to `social_links`.
 *
 * `Organization` has no `remoteUrl` field — the company site is expected to be
 * a `website` entry in `social_links`.
 */
export function getWebsiteUrl(
  links: SocialMediaItem[] | undefined | null,
): string | undefined {
  return getSocialLinkUrl(links, WEBSITE_NETWORK_ID);
}
