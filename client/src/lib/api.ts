import axios from 'axios';

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
  if (IS_MOCK) {
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
    const response = await apiClient.get<any[]>('/politicians');
    return response.data.map(politician => ({
      ...politician,
      term_start: new Date(politician.term_start),
      term_end: politician.term_end ? new Date(politician.term_end) : undefined
    }));
  } catch (error) {
    console.error('Failed to fetch politicians:', error);
    throw error;
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
    // In mock mode, we don't filter by politician - return all
    return [...mockTimelineEvents];
  }
  
  try {
    const response = await apiClient.get<TimelineEvent[]>('/timeline', {
      params: { politicianId }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch timeline events:', error);
    throw error;
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
    return response.data;
  } catch (error) {
    console.error('Failed to fetch issues:', error);
    throw error;
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
    // Basic filtering in mock mode - would be done by backend in live mode
    if (!relatedTo) return [...mockAttachments];
    return mockAttachments.filter(att => att.relatedTo === relatedTo);
  }
  
  try {
    const response = await apiClient.get<Attachment[]>('/attachments', {
      params: { relatedTo }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch attachments:', error);
    throw error;
  }
}
