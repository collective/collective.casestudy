import { describe, it, expect } from 'vitest';
import { getSocialLink, getSocialLinkUrl, getWebsiteUrl } from './socialLinks';
import type { SocialMediaItem } from '../types/content';

const website: SocialMediaItem = {
  '@id': 'urn:1',
  id: 'website',
  title: 'Company site',
  href: [{ '@id': 'https://company1.com', title: 'Company site' }],
};

const mastodon: SocialMediaItem = {
  '@id': 'urn:2',
  id: 'mastodon',
  title: 'Mastodon',
  href: [{ '@id': 'https://plone.social/@company1', title: 'Mastodon' }],
};

const links = [mastodon, website];

describe('getSocialLink', () => {
  it('finds an entry by network id', () => {
    expect(getSocialLink(links, 'website')).toBe(website);
  });

  it('returns undefined for a network that is not present', () => {
    expect(getSocialLink(links, 'github')).toBeUndefined();
  });

  it('tolerates undefined and null', () => {
    expect(getSocialLink(undefined, 'website')).toBeUndefined();
    expect(getSocialLink(null, 'website')).toBeUndefined();
  });

  it('returns the first match when a network is repeated', () => {
    const other: SocialMediaItem = { ...website, '@id': 'urn:3' };
    expect(getSocialLink([website, other], 'website')).toBe(website);
  });
});

describe('getSocialLinkUrl', () => {
  it('unwraps the object-browser href list', () => {
    expect(getSocialLinkUrl(links, 'mastodon')).toBe(
      'https://plone.social/@company1',
    );
  });

  it('returns undefined when the entry has an empty href', () => {
    const empty: SocialMediaItem = { ...website, href: [] };
    expect(getSocialLinkUrl([empty], 'website')).toBeUndefined();
  });
});

describe('getWebsiteUrl', () => {
  it('returns the website entry target', () => {
    expect(getWebsiteUrl(links)).toBe('https://company1.com');
  });

  it('returns undefined when no website entry exists', () => {
    expect(getWebsiteUrl([mastodon])).toBeUndefined();
  });

  it('returns undefined for empty social links', () => {
    expect(getWebsiteUrl([])).toBeUndefined();
  });
});
