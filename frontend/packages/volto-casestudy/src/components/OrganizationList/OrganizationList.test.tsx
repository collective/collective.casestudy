import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import OrganizationList from './OrganizationList';
import type { OrganizationSummary } from '../../types/content';

function organization(id: string, title: string): OrganizationSummary {
  return {
    '@id': `http://localhost:8080/Plone/${id}`,
    '@type': 'Organization',
    UID: `${id}-uid`,
    title,
    description: '',
    review_state: 'published',
    image_field: '',
    image_scales: null,
  } as unknown as OrganizationSummary;
}

function renderList(items: OrganizationSummary[], className?: string) {
  return render(
    <Wrapper anonymous>
      <OrganizationList items={items} className={className} />
    </Wrapper>,
  );
}

describe('OrganizationList', () => {
  it('links every organization, in order', () => {
    const { container } = renderList([
      organization('acme', 'Acme Inc.'),
      organization('globex', 'Globex'),
    ]);
    const links = container.querySelectorAll(
      '.organization-list a.organization-link',
    );
    expect(Array.from(links).map((a) => a.textContent)).toEqual([
      'Acme Inc.',
      'Globex',
    ]);
    expect(links[0].getAttribute('href')).toBe('/acme');
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderList([organization('acme', 'Acme')], 'extra');
    const classes = container.querySelector('.organization-list')?.classList;
    expect(classes?.contains('extra')).toBe(true);
  });
});
