import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import type { ComponentProps } from 'react';
import Wrapper from '@plone/volto/storybook';
import OrganizationLink from './OrganizationLink';
import type { OrganizationSummary } from '../../types/content';

const baseItem = {
  '@id': 'http://localhost:8080/Plone/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  description: '',
  review_state: 'published',
  image_field: '',
  image_scales: null,
} as unknown as OrganizationSummary;

const withLogo = {
  ...baseItem,
  image_field: 'preview_image_link',
  image_scales: {
    preview_image_link: [
      {
        'content-type': 'image/png',
        download: '@@images/image-200.png',
        filename: 'acme.png',
        width: 200,
        height: 80,
        base_path: '/logos/acme-logo',
        scales: {},
      },
    ],
  },
} as unknown as OrganizationSummary;

function renderLink(props: Partial<ComponentProps<typeof OrganizationLink>>) {
  return render(
    <Wrapper anonymous>
      <OrganizationLink item={baseItem} {...props} />
    </Wrapper>,
  );
}

describe('OrganizationLink', () => {
  it('renders the title as a link by default', () => {
    const { container } = renderLink({});
    const link = container.querySelector('a.organization-link');
    expect(link?.textContent).toBe('Acme Inc.');
    expect(link?.getAttribute('href')).toBe('/organizations/acme');
  });

  it('renders nothing without a resolvable item', () => {
    const { container } = render(
      <Wrapper anonymous>
        <OrganizationLink item={undefined as unknown as OrganizationSummary} />
      </Wrapper>,
    );
    expect(container.querySelector('.organization-link')).toBeNull();
  });

  it('renders the logo when asked for it', () => {
    const { container } = renderLink({ item: withLogo, showLogo: true });
    const img = container.querySelector('img.organization-logo');
    // `download` is relative to the linked image, named by `base_path`.
    expect(img?.getAttribute('src')).toBe(
      '/logos/acme-logo/@@images/image-200.png',
    );
    expect(img?.getAttribute('alt')).toBe('Acme Inc.');
    expect(container.querySelector('a.with-logo')).toBeTruthy();
  });

  it('resolves the logo even when the summary carries no image_field', () => {
    const { container } = renderLink({
      item: { ...withLogo, image_field: '' } as OrganizationSummary,
      showLogo: true,
    });
    expect(
      container.querySelector('img.organization-logo')?.getAttribute('src'),
    ).toBe('/logos/acme-logo/@@images/image-200.png');
  });

  it('falls back to the title when the organization has no logo', () => {
    const { container } = renderLink({ showLogo: true });
    expect(container.querySelector('img.organization-logo')).toBeNull();
    const link = container.querySelector('a.organization-link');
    expect(link?.textContent).toBe('Acme Inc.');
    expect(link?.className).toContain('with-title');
  });

  it('keeps a caller-supplied className', () => {
    const { container } = renderLink({ className: 'sidebar-entry' });
    expect(
      container.querySelector('a.organization-link.sidebar-entry'),
    ).toBeTruthy();
  });
});
