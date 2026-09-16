import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import ServicesInfo from './ServicesInfo';
import type { Organization } from '../../../types/content';

vi.mock('react-intl', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-intl')>();
  return {
    ...actual,
    useIntl: () => ({
      formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
        defaultMessage,
    }),
  };
});

const WITH_SERVICES = {
  '@id': 'http://localhost:8080/Plone/organizations/acme',
  '@type': 'Organization',
  UID: 'acme-uid',
  title: 'Acme Inc.',
  services: [
    { token: 'design', title: 'Design' },
    { token: 'dev', title: 'Development' },
    { token: 'hosting', title: 'Hosting' },
  ],
} as unknown as Organization;

function renderServices(content: Organization, className?: string) {
  return render(
    <Wrapper anonymous>
      <ServicesInfo content={content} className={className} />
    </Wrapper>,
  );
}

describe('ServicesInfo', () => {
  it('renders a heading', () => {
    const { getByText } = renderServices(WITH_SERVICES);
    expect(getByText('Services')).toBeTruthy();
  });

  it('renders one item per service', () => {
    const { container } = renderServices(WITH_SERVICES);
    expect(container.querySelectorAll('li.service-item').length).toBe(3);
  });

  it('renders the title of each service', () => {
    const { getByText } = renderServices(WITH_SERVICES);
    for (const title of ['Design', 'Development', 'Hosting']) {
      expect(getByText(title)).toBeTruthy();
    }
  });

  it('marks each item with its token as a class', () => {
    const { container } = renderServices(WITH_SERVICES);
    for (const token of ['design', 'dev', 'hosting']) {
      expect(
        container.querySelector(`li.service-item.${token}`),
      ).not.toBeNull();
    }
  });

  it('keeps the order the backend sent', () => {
    const { container } = renderServices(WITH_SERVICES);
    const titles = Array.from(
      container.querySelectorAll('li.service-item'),
      (el) => el.textContent,
    );
    expect(titles).toEqual(['Design', 'Development', 'Hosting']);
  });

  it('renders an empty list when there are no services', () => {
    const none = { ...WITH_SERVICES, services: [] } as unknown as Organization;
    const { container } = renderServices(none);
    expect(container.querySelectorAll('li.service-item').length).toBe(0);
  });

  it('survives a missing services field', () => {
    const bare = { '@id': '/acme' } as unknown as Organization;
    expect(() => renderServices(bare)).not.toThrow();
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderServices(WITH_SERVICES, 'providerInfoBlock');
    const el = container.querySelector('.services-info');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('providerInfoBlock')).toBe(true);
  });
});
