import { describe, it, expect, beforeAll } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import config from '@plone/volto/registry';
import applySocialMedia from '@plonegovbr/volto-social-media';
import OrganizationSocialLinks from './OrganizationSocialLinks';
import type { Organization } from '../../types/content';

const SOCIAL_LINKS = [
  {
    '@id': 'link-1',
    id: 'website',
    title: 'Web site',
    href: [{ '@id': 'https://acme.example', title: 'Acme' }],
  },
  {
    '@id': 'link-2',
    id: 'mastodon',
    title: 'Mastodon',
    href: [{ '@id': 'https://plone.social/@acme', title: 'Acme' }],
  },
];

const ACME = {
  '@id': 'http://localhost:8080/Plone/acme',
  '@type': 'Organization',
  title: 'Acme Inc.',
  social_links: SOCIAL_LINKS,
} as unknown as Organization;

function renderLinks(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <OrganizationSocialLinks content={content} className={className} />
    </Wrapper>,
  );
}

describe('OrganizationSocialLinks', () => {
  beforeAll(() => {
    // `SocialNetworkIcon` resolves each network through a `socialNetwork`
    // utility; the add-on registering them is not loaded by the test config.
    applySocialMedia(config);
  });

  it('renders one entry per social link', () => {
    const { container } = renderLinks(ACME);
    expect(
      container.querySelectorAll('.social-networks > li.item'),
    ).toHaveLength(2);
  });

  it('skips a social link with no target', () => {
    const noTarget = {
      ...ACME,
      social_links: [
        { '@id': 'link-1', id: 'website', title: 'Web site', href: [] },
      ],
    } as unknown as Organization;
    const { container } = renderLinks(noTarget);
    expect(
      container.querySelectorAll('.social-networks > li.item'),
    ).toHaveLength(0);
  });

  it('renders the container even with no links', () => {
    const none = { ...ACME, social_links: [] } as unknown as Organization;
    const { container } = renderLinks(none);
    expect(container.querySelector('.socialNetworks')).not.toBeNull();
  });

  it('survives content with no social_links field at all', () => {
    const bare = { '@id': '/acme' } as unknown as Organization;
    const { container } = renderLinks(bare);
    expect(container.querySelector('.socialNetworks')).not.toBeNull();
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderLinks(ACME, 'providerSocialLinks');
    const el = container.querySelector('.socialNetworks');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('providerSocialLinks')).toBe(true);
  });
});
