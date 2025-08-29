import React from 'react';

const Timeline = ({ politician }) => {
  if (!politician) return null;

  return (
    <div className="timeline" data-testid="timeline">
      <h2>Political Timeline</h2>
      <div className="timeline-item">
        <strong>Term Start:</strong> {politician.term_start}
      </div>
      <div className="timeline-item">
        <strong>Term End:</strong> {politician.term_end}
      </div>
    </div>
  );
};

export default Timeline;
