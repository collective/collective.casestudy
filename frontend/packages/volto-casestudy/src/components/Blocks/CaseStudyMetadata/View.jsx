const View = (props) => {
  const { content } = props;
  return (
    <div class="case_study_metadata">
      <h3>Case Study Metadata</h3>
      <ul>
        <li>Remote URL: {content.remoteUrl}</li>
        <li>Industry: {content.industry.title}</li>
        <li>
          Usages:{' '}
          {content.usages.map((v, index) => (
            <span key={v.token}>
              {v.title}
              {index < content.usages.length - 1 ? ', ' : ''}
            </span>
          ))}
        </li>
        <li>
          Versions:{' '}
          {content.versions.map((v, index) => (
            <span key={v.token}>
              {v.title}
              {index < content.versions.length - 1 ? ', ' : ''}
            </span>
          ))}
        </li>{' '}
      </ul>
    </div>
  );
};

export default View;
