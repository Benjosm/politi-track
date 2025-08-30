/**
 * Types for the PolitiTrack application.
 */

export interface Politician {
  id: string | number;
  name: string;
  party: string;
  office: string;
  term_start: string;
  term_end?: string;
}
