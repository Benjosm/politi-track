/**
 * Types for the PolitiTrack application.
 */

// --- Sub-interfaces for nested data structures ---

export interface Source {
  name: string;
  url?: string | null;
  retrieval_date: Date;
}

export interface PoliticalPosition {
  title: string;
  jurisdiction: string;
  start_date: Date;
  end_date?: Date | null;
  is_current: boolean;
}

export interface PartyAffiliation {
  party_name: string;
  start_date: Date;
  end_date?: Date | null;
}

export interface Vote {
  vote_date: Date;
  position: 'Yes' | 'No' | 'Abstain' | 'Not Voting'; // Using a string literal union for type safety
  bill_number: string;
  bill_title: string;
}

export interface Gift {
  description: string;
  value: number;
  report_date: Date;
  donor: string;
}

export interface CampaignDonation {
  donor_name: string;
  donor_type: string;
  amount: number;
  date: Date;
}

export interface FinancialDisclosure {
  report_year: number;
  filing_date: Date;
  document_url: string;
}

export interface CommitteeDetail {
  name: string;
  chamber: 'House' | 'Senate' | 'Joint';
}

export interface CommitteeMembership {
  role: string;
  start_date: Date;
  end_date?: Date | null;
  committee: CommitteeDetail;
}

// --- Main Interfaces for API Responses ---

/**
 * Defines the available sorting options for the politicians list.
 * This should match the `PoliticianSortBy` Enum on the backend.
 */
export type PoliticianSortBy = 
  | 'last_name_asc'
  | 'last_name_desc'
  | 'first_name_asc'
  | 'first_name_desc';

/**
 * Defines the structure for parameters used in the `getPoliticians` function.
 */
export interface GetPoliticiansParams {
  page?: number;
  size?: number;
  sortBy?: PoliticianSortBy;
  party?: string;
  jurisdiction?: string;
}

/**
 * Defines the structure of the paginated response from the GET /politicians endpoint.
 */
export interface PaginatedPoliticiansResponse {
  total: number;
  page: number;
  size: number;
  pages: number;
  results: PoliticianSummary[];
}

/**
 * A concise summary of a politician, used for search result lists.
 */
export interface PoliticianSummary {
  id: number;
  full_name: string;
  current_party?: string | null;
  current_position_title?: string | null;
  jurisdiction?: string | null;
}

/**
 * The complete, detailed profile of a politician.
 * This corresponds to the PoliticianFullDetails model on the backend.
 */
export interface PoliticianDetails {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth?: Date | null;
  biography?: string | null;
  official_website_url?: string | null;
  
  source?: Source | null;
  
  positions: PoliticalPosition[];
  party_affiliations: PartyAffiliation[];
  committee_memberships: CommitteeMembership[];
  votes: Vote[];
  gifts_received: Gift[];
  campaign_donations: CampaignDonation[];
  financial_disclosures: FinancialDisclosure[];
}

// Interface for the raw API search response structure
export interface ApiSearchResponse {
  results: PoliticianSummary[];
}
