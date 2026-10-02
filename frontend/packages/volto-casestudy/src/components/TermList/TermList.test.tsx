import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import TermList from './TermList';

const TERMS = [
  { token: 'portal', title: 'Portal' },
  { token: 'intranet', title: 'Intranet' },
];

describe('TermList', () => {
  it('joins the terms with commas', () => {
    const { container } = render(<TermList terms={TERMS} />);
    expect(container.textContent).toBe('Portal, Intranet');
  });

  it('does not leave a trailing comma on a single term', () => {
    const { container } = render(<TermList terms={[TERMS[0]]} />);
    expect(container.textContent).toBe('Portal');
  });

  it('marks each term with its token as a class', () => {
    const { container } = render(<TermList terms={TERMS} />);
    expect(container.querySelector('.term.portal')).not.toBeNull();
    expect(container.querySelector('.term.intranet')).not.toBeNull();
  });

  it('renders inline, so it can sit inside a paragraph', () => {
    const { container } = render(<TermList terms={TERMS} className="extra" />);
    const root = container.firstElementChild;
    expect(root?.tagName).toBe('SPAN');
    expect(root?.classList.contains('term-list')).toBe(true);
    expect(root?.classList.contains('extra')).toBe(true);
  });

  it('renders nothing visible for no terms', () => {
    const { container } = render(<TermList terms={[]} />);
    expect(container.textContent).toBe('');
  });
});
