// No imports needed - using native fetch API

// Base URL for the API - this would typically be configured based on environment
const API_BASE_URL = '/api';

/**
 * Searches for politicians based on a query string
 * @param {string} query - The search query (e.g., name, party, district)
 * @returns {Promise<Array>} A promise that resolves to an array of politician objects
 * @throws {Error} When the API request fails
 */
export async function searchPoliticians(query) {
  try {
    // Validate input
    if (!query || typeof query !== 'string') {
      throw new Error('Search query is required and must be a string');
    }

    // Encode the query to handle special characters
    const encodedQuery = encodeURIComponent(query.trim());

    // Make the API request
    const response = await fetch(`/search?q=${encodedQuery}`);

    // Check if the response is ok (status in the range 200-299)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    // Parse and return the JSON data
    const data = await response.json();
    return data;
  } catch (error) {
    // Re-throw the error for the calling code to handle
    console.error('Error searching politicians:', error);
    throw error;
  }
}
