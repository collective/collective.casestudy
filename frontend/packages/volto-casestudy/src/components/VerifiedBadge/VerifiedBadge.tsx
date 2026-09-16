import React from 'react';
import VerifiedIcon from '@plone-collective/volto-casestudy/icons/verified.svg';
import Icon from '@plone/volto/components/theme/Icon/Icon';
import './verified-badge.scss';

export interface VerifiedBadgeProps {
  /** Extra classes for the container. */
  className?: string;
}

export const VerifiedBadge = ({ className }: VerifiedBadgeProps) => {
  const classes = ['verified-badge'];
  if (className) classes.push(className);

  return <Icon name={VerifiedIcon} className={classes.join(' ')} />;
};

export default VerifiedBadge;
