import { TimelineEvent, FinancialDisclosure } from '../lib/types';

export const mockTimelineEvents: TimelineEvent[] = [
  {
    id: 1,
    year: 2020,
    type: "Election",
    title: "Ran for Senate",
    description: "Campaign focused on healthcare reform",
    financialData: [
      {
        amount: 500000,
        category: "Donations",
        source: "Individuals"
      },
      {
        amount: 250000,
        category: "PAC Contributions",
        source: "Healthcare PAC"
      }
    ]
  },
  {
    id: 2,
    year: 2021,
    type: "Legislation",
    title: "Introduced Clean Energy Bill",
    description: "Proposed comprehensive climate change legislation",
    financialData: [
      {
        amount: 75000,
        category: "Travel Expenses",
        source: "Personal Funds"
      }
    ]
  }
];

export const mockFinancialDisclosures: FinancialDisclosure[] = [
  {
    amount: 50000,
    category: "Stocks",
    source: "Previous Investments"
  },
  {
    amount: 25000,
    category: "Real Estate",
    source: "Property Sales"
  }
];
