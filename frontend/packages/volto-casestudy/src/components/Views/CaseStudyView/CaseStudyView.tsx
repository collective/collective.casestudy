import React from 'react';
import { getBaseUrl } from '@plone/volto/helpers/Url/Url';
import { Container } from '@plone/components';
import RenderBlocks from '@plone/volto/components/theme/View/RenderBlocks';
import type { CaseStudy } from '@plone-collective/volto-casestudy/types/content';

interface CaseStudyViewProps {
  content: CaseStudy;
  location?: {
    pathname: string;
  };
  [key: string]: any;
}

const CaseStudyView: React.FC<CaseStudyViewProps> = (props) => {
  const { location } = props;
  const path = getBaseUrl(location?.pathname || '');

  return (
    <Container
      id="page-document"
      className="view-wrapper ui container casestudy-view"
    >
      <RenderBlocks {...props} path={path} />
    </Container>
  );
};

export default CaseStudyView;
