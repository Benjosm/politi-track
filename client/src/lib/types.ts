/**
 * Types for the PolitiTrack application.
 */

export interface Politician {
  id: number;
  name: string;
  party: string;
  office: string;
  term_start: Date;
  term_end?: Date;
}

export interface FinancialDisclosure {
  amount: number;
  category: string;
  source: string;
}

export interface TimelineEvent {
  id: number;
  year: number;
  type: string;
  title: string;
  description: string;
  financialData: FinancialDisclosure[];
}

export interface Issue {
  id: number;
  title: string;
  description: string;
  category: string;
  relatedPoliticians: number[];
  timelineEvents: number[];
}

export interface Attachment {
  id: number;
  name: string;
  url: string;
  type: string;
  size: number;
  uploadDate: string;
  relatedTo: string;
}
