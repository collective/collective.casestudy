import React from 'react';
import cx from 'classnames';
import { Container } from '@plone/components';
import { slugify } from '@plone/volto/helpers/Utils/Utils';
import './info-box.scss';

export interface InfoBoxProps {
  /**
   * Identifies the box. It gets the slugified name as a class of its own
   * plus `<name>-info`; its heading gets `<name>Title` and the values
   * wrapper `<name>Wrapper`.
   */
  name: string;
  /** Heading text, already translated. */
  title: string;
  /** Element wrapping the values. */
  as?: 'p' | 'ul' | 'div';
  /** Extra classes for the container. */
  className?: string;
  children: React.ReactNode;
}

/**
 * One labelled box of information: a heading over a wrapper holding the
 * values, with a border on top. The shared base of every info block.
 */
export const InfoBox = ({
  name,
  title,
  as: Wrapper = 'p',
  className,
  children,
}: InfoBoxProps) => (
  <Container
    className={cx('info-box', slugify(name), `${name}-info`, className)}
  >
    <h2 className={`blockTitle ${name}Title`}>{title}</h2>
    <Wrapper className={`${name}Wrapper`}>{children}</Wrapper>
  </Container>
);

export default InfoBox;
