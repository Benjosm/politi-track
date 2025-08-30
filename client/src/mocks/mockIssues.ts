import { Issue } from '../lib/types';

export const mockIssues: Issue[] = [
  {
    id: 1,
    title: "Universal Healthcare",
    description: "Proposal for a single-payer healthcare system",
    category: "Healthcare",
    relatedPoliticians: [1, 2],
    timelineEvents: [1]
  },
  {
    id: 2,
    title: "Climate Action Plan",
    description: "Comprehensive strategy for carbon neutrality by 2050",
    category: "Environment",
    relatedPoliticians: [2],
    timelineEvents: [2]
  },
  {
    id: 3,
    title: "Infrastructure Investment",
    description: "Plan for rebuilding roads, bridges, and public transit",
    category: "Economy",
    relatedPoliticians: [1],
    timelineEvents: []
  }
];
