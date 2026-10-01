import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import InfoBox from './InfoBox';

describe('InfoBox', () => {
  it('derives its class names from the name', () => {
    const { container } = render(
      <InfoBox name="usage" title="Usage">
        Portal
      </InfoBox>,
    );
    const box = container.querySelector('.info-box.usage-info');
    expect(box).not.toBeNull();
    expect(box?.querySelector('h2.blockTitle.usageTitle')?.textContent).toBe(
      'Usage',
    );
    expect(box?.querySelector('.usageWrapper')?.textContent).toBe('Portal');
  });

  it('wraps the values in a paragraph by default', () => {
    const { container } = render(
      <InfoBox name="usage" title="Usage">
        Portal
      </InfoBox>,
    );
    expect(container.querySelector('.usageWrapper')?.tagName).toBe('P');
  });

  it('uses the requested wrapper element', () => {
    const { container } = render(
      <InfoBox name="services" title="Services" as="ul">
        <li>Design</li>
      </InfoBox>,
    );
    expect(container.querySelector('.servicesWrapper')?.tagName).toBe('UL');
  });

  it('appends a caller class without dropping its own', () => {
    const { container } = render(
      <InfoBox name="usage" title="Usage" className="metadata-box">
        Portal
      </InfoBox>,
    );
    const classes = container.querySelector('.usage-info')?.classList;
    expect(classes?.contains('info-box')).toBe(true);
    expect(classes?.contains('metadata-box')).toBe(true);
  });

  it('carries the slugified name as a class', () => {
    const { container } = render(
      <InfoBox name="versions" title="Versions">
        Plone 6.0
      </InfoBox>,
    );
    const box = container.querySelector('.info-box');
    expect(box?.classList.contains('versions')).toBe(true);
  });

  it('slugifies a name that is not a plain identifier', () => {
    const { container } = render(
      <InfoBox name="Case Study-Usages" title="Usages">
        Portal
      </InfoBox>,
    );
    const box = container.querySelector('.info-box');
    expect(box?.classList.contains('case_study_usages')).toBe(true);
  });
});
