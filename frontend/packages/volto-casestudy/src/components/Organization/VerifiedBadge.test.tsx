import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Wrapper from '@plone/volto/storybook';
import VerifiedBadge from './VerifiedBadge';

function renderBadge(props: { className?: string } = {}) {
  return render(
    <Wrapper anonymous>
      <VerifiedBadge {...props} />
    </Wrapper>,
  );
}

describe('VerifiedBadge', () => {
  it('renders an icon', () => {
    const { container } = renderBadge();
    expect(container.querySelector('svg')).not.toBeNull();
  });

  it('always carries its own class', () => {
    const { container } = renderBadge();
    expect(container.querySelector('.verified-badge')).not.toBeNull();
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = renderBadge({ className: 'providerBadge' });
    const el = container.querySelector('.verified-badge');
    expect(el).not.toBeNull();
    expect(el?.classList.contains('providerBadge')).toBe(true);
  });

  it('renders nothing extra when no class is given', () => {
    const { container } = renderBadge();
    const el = container.querySelector('.verified-badge');
    // `undefined` must not reach the class list as a literal.
    expect(el?.className).not.toContain('undefined');
  });
});
