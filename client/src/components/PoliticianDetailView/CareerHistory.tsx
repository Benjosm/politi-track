// src/components/PoliticianDetailView/CareerHistory.tsx

import React from 'react';
import { PoliticianDetails } from '../../lib/types';
import InfoCard from './InfoCard';
import { CareerIcon } from './Icons';

const formatDate = (date: Date) => date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });

const CareerHistory: React.FC<{ politician: PoliticianDetails }> = ({ politician }) => {
  return (
    <InfoCard title="Career History" icon={<CareerIcon />}>
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">Political Positions</h3>
          <ul className="divide-y divide-gray-200 dark:divide-gray-700">
            {politician.positions.map((pos, i) => (
              <li key={i} className="py-3">
                <p className="font-bold">{pos.title}</p>
                <p className="text-gray-600 dark:text-gray-400">{pos.jurisdiction}</p>
                <p className="text-sm text-gray-500">
                  {formatDate(pos.start_date)} - {pos.end_date ? formatDate(pos.end_date) : 'Present'}
                </p>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">Party Affiliations</h3>
          <ul className="divide-y divide-gray-200 dark:divide-gray-700">
            {politician.party_affiliations.map((party, i) => (
              <li key={i} className="py-3">
                <p className="font-bold">{party.party_name} Party</p>
                <p className="text-sm text-gray-500">
                  {formatDate(party.start_date)} - {party.end_date ? formatDate(party.end_date) : 'Present'}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </InfoCard>
  );
};

export default CareerHistory;
