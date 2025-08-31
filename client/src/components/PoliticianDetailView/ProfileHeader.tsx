// src/components/PoliticianDetailView/ProfileHeader.tsx

import React from 'react';
import { PoliticianDetails } from '../../lib/types';

const ProfileHeader: React.FC<{ politician: PoliticianDetails }> = ({ politician }) => {
  const currentPosition = politician.positions.find(p => p.is_current);
  const currentParty = politician.party_affiliations.find(p => !p.end_date);

  return (
    <div className="flex flex-col sm:flex-row items-start mb-8">
      <img 
        src={`https://i.pravatar.cc/150?u=${politician.id}`} 
        alt={`${politician.first_name} ${politician.last_name}`}
        className="w-32 h-32 rounded-full mr-8 mb-4 sm:mb-0 border-4 border-gray-200 dark:border-gray-700 shadow-lg"
      />
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white">{politician.first_name} {politician.last_name}</h1>
        {currentPosition && (
          <p className="text-xl text-blue-600 dark:text-blue-400 font-semibold">{currentPosition.title} for {currentPosition.jurisdiction}</p>
        )}
        {currentParty && (
          <p className="text-lg text-gray-600 dark:text-gray-400">{currentParty.party_name} Party</p>
        )}
        {politician.biography && (
            <p className="mt-4 text-gray-600 dark:text-gray-300 max-w-2xl">{politician.biography}</p>
        )}
      </div>
    </div>
  );
};

export default ProfileHeader;
