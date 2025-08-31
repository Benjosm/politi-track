// src/components/PoliticianDetailView/FinancialsAndEthics.tsx

import React from 'react';
import { PoliticianDetails } from '../../lib/types';
import InfoCard from './InfoCard';
import { GiftIcon, DonationIcon } from './Icons';

const formatDate = (date: Date) => date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
const formatCurrency = (amount: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

const FinancialsAndEthics: React.FC<{ politician: PoliticianDetails }> = ({ politician }) => {
  return (
    <div className="space-y-8">
      <InfoCard title="Reported Gifts" icon={<GiftIcon />}>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Date</th>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Donor</th>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Description</th>
                <th className="px-4 py-2 text-right text-xs font-medium uppercase">Value</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {politician.gifts_received.length > 0 ? politician.gifts_received.map((gift, i) => (
                <tr key={i}>
                  <td className="px-4 py-3 whitespace-nowrap">{formatDate(gift.report_date)}</td>
                  <td className="px-4 py-3">{gift.donor}</td>
                  <td className="px-4 py-3">{gift.description}</td>
                  <td className="px-4 py-3 text-right whitespace-nowrap font-mono">{formatCurrency(gift.value)}</td>
                </tr>
              )) : (
                <tr><td colSpan={4} className="px-4 py-3 text-center text-gray-500">No gifts reported.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </InfoCard>

      <InfoCard title="Campaign Donations" icon={<DonationIcon />}>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Date</th>
                <th className="px-4 py-2 text-left text-xs font-medium uppercase">Donor</th>
                <th className="px-4 py-2 text-right text-xs font-medium uppercase">Amount</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {politician.campaign_donations.length > 0 ? politician.campaign_donations.slice(0, 10).map((donation, i) => ( // Display top 10 for brevity
                <tr key={i}>
                  <td className="px-4 py-3 whitespace-nowrap">{formatDate(donation.date)}</td>
                  <td className="px-4 py-3">{donation.donor_name}</td>
                  <td className="px-4 py-3 text-right whitespace-nowrap font-mono">{formatCurrency(donation.amount)}</td>
                </tr>
              )) : (
                <tr><td colSpan={3} className="px-4 py-3 text-center text-gray-500">No donation records found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </InfoCard>
    </div>
  );
};

export default FinancialsAndEthics;
