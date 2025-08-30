import React from 'react';
import { Politician } from '../lib/types';

interface TimelineProps {
  politician: Politician;
}

const Timeline: React.FC<TimelineProps> = ({ politician }) => {
  if (!politician) return null;

  return (
    <div className="timeline" data-testid="timeline">
      <h2>Political Timeline</h2>
      <div className="timeline-item">
        <strong>Term Start:</strong> {politician.term_start}
      </div>
      <div className="timeline-item">
        <strong>Term End:</strong> {politician.term_end || 'Present'}
      </div>
    </div>
  );
};

export default Timeline;
