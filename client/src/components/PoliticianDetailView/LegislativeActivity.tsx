// src/components/PoliticianDetailView/LegislativeActivity.tsx

import React from 'react';
import { PoliticianDetails } from '../../lib/types';
import InfoCard from './InfoCard';
import { VoteIcon, CommitteeIcon } from './Icons'; // Simple SVG icon components

const formatDate = (date: Date) => date.toLocaleDateString();

const LegislativeActivity: React.FC<{ politician: PoliticianDetails }> = ({ politician }) => {
  return (
    <div className="space-y-6">
      <InfoCard title="Voting Record" icon={<VoteIcon />}>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Date</th>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Bill</th>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Position</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {politician.votes.length > 0 ? politician.votes.map((vote, i) => (
                <tr key={i}>
                  <td className="px-4 py-3 whitespace-nowrap">{formatDate(vote.vote_date)}</td>
                  <td className="px-4 py-3">{vote.bill_title} ({vote.bill_number})</td>
                  <td className="px-4 py-3 font-semibold">{vote.position}</td>
                </tr>
              )) : <tr><td colSpan={3} className="px-4 py-3 text-center">No voting records found.</td></tr>}
            </tbody>
          </table>
        </div>
      </InfoCard>

      <InfoCard title="Committee Assignments" icon={<CommitteeIcon />}>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Committee</th>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Role</th>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Term</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {politician.committee_memberships.length > 0 ? politician.committee_memberships.map((cm, i) => (
                <tr key={i}>
                  <td className="px-4 py-3 whitespace-nowrap font-semibold">{cm.committee.name}</td>
                  <td className="px-4 py-3 whitespace-nowrap">{cm.role}</td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    {formatDate(cm.start_date)} - {cm.end_date ? formatDate(cm.end_date) : 'Present'}
                  </td>
                </tr>
              )) : (
                <tr>
                  <td colSpan={3} className="px-4 py-3 text-center text-gray-500">
                    No committee assignments found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </InfoCard>
    </div>
  );
};

export default LegislativeActivity;
