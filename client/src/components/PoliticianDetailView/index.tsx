// src/components/PoliticianDetailView/index.tsx

import React from 'react';
import { PoliticianDetails } from '../../lib/types';
import ProfileHeader from './ProfileHeader';
import LegislativeActivity from './LegislativeActivity';
import CareerHistory from './CareerHistory';
import FinancialsAndEthics from './FinancialsAndEthics';

interface PoliticianDetailViewProps {
  politician: PoliticianDetails;
  onBack: () => void;
}

const PoliticianDetailView: React.FC<PoliticianDetailViewProps> = ({ politician, onBack }) => {
  return (
    <div className="bg-gray-100 dark:bg-gray-800/50 rounded-lg shadow-xl p-6 sm:p-8 w-full animate-fade-in space-y-8">
      <button
        className="text-blue-600 dark:text-blue-400 hover:underline mb-4"
        onClick={onBack}
      >
        ← Back to Search
      </button>
      
      <ProfileHeader politician={politician} />
      
      <div className="grid grid-cols-1 gap-8">
        <CareerHistory politician={politician} />
        <LegislativeActivity politician={politician} />
        <FinancialsAndEthics politician={politician} />
      </div>
    </div>
  );
};

export default PoliticianDetailView;
