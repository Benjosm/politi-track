// src/components/PoliticianDetailView/InfoCard.tsx

import React from 'react';

interface InfoCardProps {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}

const InfoCard: React.FC<InfoCardProps> = ({ title, icon, children }) => (
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 w-full">
    <div className="flex items-center mb-4">
      <div className="text-blue-500 dark:text-blue-400 mr-3">{icon}</div>
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{title}</h2>
    </div>
    <div className="text-gray-700 dark:text-gray-300 space-y-4">{children}</div>
  </div>
);

export default InfoCard;
