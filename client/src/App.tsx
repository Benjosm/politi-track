import React, { useState, useEffect } from 'react';
import { searchPoliticians } from './lib/api';
import SearchBar from './components/SearchBar';
import Timeline from './components/Timeline';
import { Politician } from './lib/types';
import { mockTimelineEvents } from './mocks/mockTimelineEvents';
import TestApi from './TestApi';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Politician[]>([]);
  const [activePolitician, setActivePolitician] = useState<Politician | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Formats term dates to show year ranges (e.g., "2020 - Present")
   * @param {Date} termStart - The start date as Date object
   * @param {Date | undefined} termEnd - The end date as Date object (optional)
   * @returns {string} Formatted year range
   */
  const formatTermDates = (termStart: Date, termEnd?: Date): string => {
    const startValid = !isNaN(termStart.getTime());
    const startYear = startValid ? termStart.getFullYear() : '';
  
    if (!startValid) {
      return '';
    }
  
    if (!termEnd) {
      return `${startYear} - Present`;
    }
  
    const endValid = !isNaN(termEnd.getTime());
    const endYear = endValid ? termEnd.getFullYear() : 'Present';
  
    return `${startYear} - ${endYear}`;
  };

  /**
   * Handles the search operation when the user submits a query
   * @param {string} query - The search query to look up
   */
  const handleSearch = async (query: string) => {
    // Set loading state and clear previous error
    setSearchQuery(query);
    setIsLoading(true);
    setError(null);

    try {
      // Call the API to search for politicians
      const results: Politician[] = await searchPoliticians(query);
      
      // Update state with the search results and reset active politician
      setSearchResults(results);
      setActivePolitician(null);
    } catch (err) {
      // Handle any errors from the API call
      setError('Failed to search politicians. Please try again later.');
      console.error('Search error:', err);
    } finally {
      // Always set loading to false when the operation completes
      setIsLoading(false);
    }
  };

  // Check for test query parameter
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const testParam = urlParams.get('test');
    
    if (testParam === 'api') {
      document.title = 'API Wrapper Test';
    }
  }, []);

  return (
    <div className="App">
      {/* Check for test query parameter */}
      {new URLSearchParams(window.location.search).get('test') === 'api' ? (
        <TestApi />
      ) : (
        <>
          {activePolitician ? (
            // Detail View
            <div className="politician-detail">
              <button className="back-button" onClick={() => setActivePolitician(null)}>
                ← Back to Search
              </button>
              <h1>{activePolitician.name}</h1>
              <p><strong>Party:</strong> {activePolitician.party}</p>
              <p><strong>Office:</strong> {activePolitician.office}</p>
              <p><strong>Term:</strong> {formatTermDates(activePolitician.term_start, activePolitician.term_end)}</p>
              <Timeline politician={activePolitician} events={mockTimelineEvents} />
            </div>
          ) : (
            // Search/Home View
            <div className="search-view">
              <header className="app-header">
                <h1>PolitiTrack</h1>
              </header>
              <SearchBar onSearch={handleSearch} onResults={setSearchResults} onError={setError} />
              {isLoading ? (
                <p>Loading...</p>
              ) : error ? (
                <p className="error-message">{error}</p>
              ) : searchResults.length > 0 ? (
                <div className="results-grid">
                  {searchResults.map((politician) => (
                    <div
                      key={politician.id}
                      className="politician-card"
                      onClick={() => setActivePolitician(politician)}
                    >
                      <h3>{politician.name}</h3>
                      <p>{politician.party} - {politician.office}</p>
                      <p>{formatTermDates(politician.term_start, activePolitician.term_end)}</p>
                    </div>
                  ))}
                </div>
              ) : searchQuery ? (
                <p>No results found for "{searchQuery}"</p>
              ) : (
                <p>Enter a name to search for politicians</p>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;
