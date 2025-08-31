import axios from 'axios';
import { ApiSearchResponse, GetPoliticiansParams, PaginatedPoliticiansResponse, PoliticianDetails, PoliticianSummary } from './types';

// Configuration using Vite environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const IS_MOCK = import.meta.env.VITE_API_MOCK === 'true';

// Create the configured axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000, // 15 second timeout for production readiness
});

// Placeholder for future mock mode implementation
if (IS_MOCK) {
  // In future iterations, we'll add mock adapter setup here
  console.debug('API client running in mock mode (configuration ready)');
}

// Add request interceptor for global request modifications
apiClient.interceptors.request.use(
  (config) => {
    // Could add authentication tokens here in production implementation
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for global error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error(`API Error [${error.response.status}]:`, error.response.data);
    } else if (error.request) {
      console.error('Network error:', error.message);
    } else {
      console.error('API setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

export { apiClient };

// Import mock data (will only be loaded when IS_MOCK is true)
let mockPoliticianSummaries: typeof import('../mocks/mockPoliticianSummaries').mockPoliticianSummaries;
let mockPoliticianDetails: typeof import('../mocks/mockPoliticians').mockPoliticianDetails;

// Dynamically import mock data when needed
async function loadMockData() {
  if (IS_MOCK && !mockPoliticianSummaries) { // Prevent re-importing
    const mocks = await import('../mocks/mockPoliticianSummaries');
    mockPoliticianSummaries = mocks.mockPoliticianSummaries;
    mockPoliticianDetails = (await import('../mocks/mockPoliticians')).mockPoliticianDetails;
  }
}

/**
 * Searches for politicians based on a query string.
 * @param query The search term.
 * @returns Promise resolving to a list of matching politician summaries.
 */
export async function searchPoliticians(query: string): Promise<PoliticianSummary[]> {
  if (!query || query.trim() === '') {
    return [];
  }
  
  if (IS_MOCK) {
    await loadMockData();
    const lowerCaseQuery = query.toLowerCase();
    return mockPoliticianSummaries.filter(p =>
      p.full_name.toLowerCase().includes(lowerCaseQuery)
    );
  }

  try {
    const response = await apiClient.get<ApiSearchResponse>('/search', {
      params: { q: query }
    });
    // The API directly returns the correct structure, no date conversion is needed for the summary.
    return response.data.results || [];
  } catch (error) {
    console.error(`Failed to search for politicians with query "${query}":`, error);
    return []; // Return empty array on error
  }
}

/**
 * Fetches the complete, detailed profile for a single politician by their ID.
 * @param politicianId The unique ID of the politician.
 * @returns Promise resolving to the full politician details, or null if not found or on error.
 */
export async function getPoliticianDetails(politicianId: number): Promise<PoliticianDetails | null> {
  if (IS_MOCK) {
    await loadMockData();
    return mockPoliticianDetails.find(politician => politician.id === politicianId) ?? null;
  }

  try {
    const response = await apiClient.get<any>(`/politicians/${politicianId}`);
    const data = response.data;


    // "Hydrate" the raw JSON data, converting all date strings to Date objects.
    // This ensures the final object conforms to our detailed TypeScript interface.
    const hydratedDetails: PoliticianDetails = {
      ...data,
      date_of_birth: data.date_of_birth ? new Date(data.date_of_birth) : null,
      source: data.source ? { ...data.source, retrieval_date: new Date(data.source.retrieval_date) } : null,
      
      positions: data.positions.map((p: any) => ({
        ...p,
        start_date: new Date(p.start_date),
        end_date: p.end_date ? new Date(p.end_date) : null,
      })),

      party_affiliations: data.party_affiliations.map((p: any) => ({
        ...p,
        start_date: new Date(p.start_date),
        end_date: p.end_date ? new Date(p.end_date) : null,
      })),
      
      committee_memberships: data.committee_memberships.map((cm: any) => ({
        ...cm,
        start_date: new Date(cm.start_date),
        end_date: cm.end_date ? new Date(cm.end_date) : null,
      })),

      votes: data.votes.map((v: any) => ({
        ...v,
        vote_date: new Date(v.vote_date),
      })),
      
      gifts_received: data.gifts_received.map((g: any) => ({
        ...g,
        report_date: new Date(g.report_date),
      })),
      
      campaign_donations: data.campaign_donations.map((cd: any) => ({
        ...cd,
        date: new Date(cd.date),
      })),
      
      financial_disclosures: data.financial_disclosures.map((fd: any) => ({
        ...fd,
        filing_date: new Date(fd.filing_date),
      })),
    };

    return hydratedDetails;
    
  } catch (error: any) {
    // It's good practice to check for a 404 status specifically
    if (error.response && error.response.status === 404) {
      console.warn(`Politician with ID ${politicianId} not found.`);
    } else {
      console.error(`Failed to fetch details for politician ${politicianId}:`, error);
    }
    return null; // Return null on any error
  }
}

/**
 * Fetches a paginated, filterable, and sortable list of politicians.
 * @param params - Optional parameters for pagination, sorting, and filtering.
 * @returns A promise resolving to a paginated response object.
 */
export async function getPoliticians(
  params: GetPoliticiansParams = {}
): Promise<PaginatedPoliticiansResponse> {
  await loadMockData();

  if (IS_MOCK) {
    let results = [...mockPoliticianSummaries];
    const { page = 1, size = 10, sortBy = 'last_name_asc', party, jurisdiction } = params;

    // Filtering
    if (party) {
      results = results.filter(p => p.current_party?.toLowerCase() === party.toLowerCase());
    }
    if (jurisdiction) {
      results = results.filter(p => p.jurisdiction?.toLowerCase() === jurisdiction.toLowerCase());
    }

    // Sorting
    results.sort((a, b) => {
      const [field, direction] = sortBy.split('_');
      const valA = (field === 'last_name' ? a.full_name.split(' ').pop() : a.full_name.split(' ')[0]) || '';
      const valB = (field === 'last_name' ? b.full_name.split(' ').pop() : b.full_name.split(' ')[0]) || '';
      
      if (valA < valB) return direction === 'asc' ? -1 : 1;
      if (valA > valB) return direction === 'asc' ? 1 : -1;
      return 0;
    });

    const total = results.length;
    const paginatedResults = results.slice((page - 1) * size, page * size);
    
    return {
      total,
      page,
      size,
      pages: Math.ceil(total / size),
      results: paginatedResults
    };
  }

  try {
    // The backend endpoint uses 'sort_by', so we map our 'sortBy' parameter.
    const { sortBy, ...otherParams } = params;
    const apiParams = {
      ...otherParams,
      ...(sortBy && { sort_by: sortBy }), // Only add sort_by if sortBy is provided
    };

    const response = await apiClient.get<PaginatedPoliticiansResponse>('/politicians', {
      params: apiParams
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch politicians:', error);
    // Return a default empty state to prevent UI crashes
    return {
      total: 0,
      page: params.page || 1,
      size: params.size || 10,
      pages: 0,
      results: [],
    };
  }
}
