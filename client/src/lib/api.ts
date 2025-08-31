import axios from 'axios';
import { Attachment, Issue, Politician, TimelineEvent } from './types';

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
let mockPoliticians: typeof import('../mocks/mockPoliticians').mockPoliticians;
let mockTimelineEvents: typeof import('../mocks/mockTimelineEvents').mockTimelineEvents;
let mockIssues: typeof import('../mocks/mockIssues').mockIssues;
let mockAttachments: typeof import('../mocks/mockAttachments').mockAttachments;

// Dynamically import mock data when needed
async function loadMockData() {
  if (IS_MOCK && !mockPoliticians) { // Prevent re-importing
    const mocks = await import('../mocks/mockPoliticians');
    mockPoliticians = mocks.mockPoliticians;
    mockTimelineEvents = (await import('../mocks/mockTimelineEvents')).mockTimelineEvents;
    mockIssues = (await import('../mocks/mockIssues')).mockIssues;
    mockAttachments = (await import('../mocks/mockAttachments')).mockAttachments;
  }
}

/**
 * Fetches a list of politicians
 * @returns Promise resolving to Politician[]
 */
export async function getPoliticians(): Promise<Politician[]> {
  await loadMockData();
  if (IS_MOCK) return [...mockPoliticians];

  try {
    const response = await apiClient.get<Politician[]>('/politicians');
    // Default to an empty array if response.data is falsy
    return (response.data || []).map(politician => ({
      ...politician,
      term_start: new Date(politician.term_start),
      term_end: politician.term_end ? new Date(politician.term_end) : undefined
    }));
  } catch (error) {
    console.error('Failed to fetch politicians:', error);
    return []; // Return empty array on error
  }
}

/**
 * Fetches timeline events for a politician
 * @param politicianId Optional politician ID to filter by
 * @returns Promise resolving to TimelineEvent[]
 */
export async function getTimelineEvents(politicianId?: number): Promise<TimelineEvent[]> {
  await loadMockData();
  if (IS_MOCK) {
    return [...mockTimelineEvents];
  }

  try {
    const response = await apiClient.get<TimelineEvent[]>('/timeline', {
      params: { politicianId }
    });
    // Default to an empty array if response.data is falsy
    return response.data || [];
  } catch (error) {
    console.error('Failed to fetch timeline events:', error);
    return []; // Return empty array on error
  }
}

/**
 * Fetches a list of political issues
 * @returns Promise resolving to Issue[]
 */
export async function getIssues(): Promise<Issue[]> {
  await loadMockData();
  if (IS_MOCK) return [...mockIssues];

  try {
    const response = await apiClient.get<Issue[]>('/issues');
    // Default to an empty array if response.data is falsy
    return response.data || [];
  } catch (error) {
    console.error('Failed to fetch issues:', error);
    return []; // Return empty array on error
  }
}

/**
 * Fetches attachments related to various entities
 * @param relatedTo Optional filter for attachments related to specific entity type/ID
 * @returns Promise resolving to Attachment[]
 */
export async function getAttachments(relatedTo?: string): Promise<Attachment[]> {
  await loadMockData();
  if (IS_MOCK) {
    if (!relatedTo) return [...mockAttachments];
    return mockAttachments.filter(att => att.relatedTo === relatedTo);
  }

  try {
    const response = await apiClient.get<Attachment[]>('/attachments', {
      params: { relatedTo }
    });
    // Default to an empty array if response.data is falsy
    return response.data || [];
  } catch (error) {
    console.error('Failed to fetch attachments:', error);
    return []; // Return empty array on error
  }
}

/**
 * Searches for politicians based on a query string.
 * @param query The search term.
 * @returns Promise resolving to a list of matching Politician objects.
 */
export async function searchPoliticians(query: string): Promise<Politician[]> {
  if (!query || query.trim() === '') {
    return [];
  }

  await loadMockData();

  if (IS_MOCK) {
    const lowerCaseQuery = query.toLowerCase();
    return mockPoliticians.filter(p =>
      p.name.toLowerCase().includes(lowerCaseQuery)
    );
  }

  try {
    const response = await apiClient.get<Politician[]>('/search', {
      params: { q: query }
    });
    // Default to an empty array if response.data is falsy
    return (response.data || []).map(politician => ({
      ...politician,
      term_start: new Date(politician.term_start),
      term_end: politician.term_end ? new Date(politician.term_end) : undefined,
    }));
  } catch (error) {
    console.error(`Failed to search for politicians with query "${query}":`, error);
    return []; // Return empty array on error
  }
}
