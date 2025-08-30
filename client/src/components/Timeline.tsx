import React from 'react';
import { Politician, TimelineEvent } from '../lib/types';

interface TimelineProps {
  politician: Politician;
  events: TimelineEvent[];
}

const Timeline: React.FC<TimelineProps> = ({ politician, events }) => {
  if (!politician) return null;

  return (
    <div className="timeline" data-testid="timeline">
      <h2>Political Timeline</h2>
      <div className="timeline-item">
        <strong>Term Start:</strong> {politician.term_start.getFullYear()}
      </div>
      <div className="timeline-item">
        <strong>Term End:</strong> {politician.term_end ? politician.term_end.getFullYear() : 'Present'}
      </div>
      <h3>Key Events</h3>
      {events.length === 0 ? (
        <p>No events to display.</p>
      ) : (
        <ul>
          {events.map((event) => (
            <li key={event.id} className="timeline-event">
              <strong>{event.year} - {event.title}</strong> ({event.type})
              <p>{event.description}</p>
              {event.financialData.length > 0 && (
                <div className="financial-data">
                  <strong>Financial Disclosures:</strong>
                  <ul>
                    {event.financialData.map((disclosure, index) => (
                      <li key={index}>
                        ${disclosure.amount.toLocaleString()} from {disclosure.source} ({disclosure.category})
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Timeline;
