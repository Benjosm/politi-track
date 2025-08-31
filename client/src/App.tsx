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

  const formatTermDates = (termStart: Date, termEnd?: Date): string => {
    const startYear = termStart.getFullYear();
    const endYear = termEnd ? termEnd.getFullYear() : 'Present';
    return `${startYear} - ${endYear}`;
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    setIsLoading(true);
    setError(null);
    setSearchResults([]);
    setActivePolitician(null);

    try {
      const results: Politician[] = await searchPoliticians(query);
      setSearchResults(results);
    } catch (err) {
      setError('Failed to search politicians. Please try again later.');
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const testParam = urlParams.get('test');
    if (testParam === 'api') {
      document.title = 'API Wrapper Test';
    }
  }, []);

  if (new URLSearchParams(window.location.search).get('test') === 'api') {
    return <TestApi />;
  }

  return (
    <div className="min-h-screen font-sans text-gray-800 dark:text-gray-200 p-4 sm:p-8">
      <div className="container mx-auto max-w-5xl">
        {activePolitician ? (
          // Detail View
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 sm:p-8 w-full animate-fade-in">
            <button
              className="text-blue-600 dark:text-blue-400 hover:underline mb-6"
              onClick={() => setActivePolitician(null)}
            >
              ← Back to Search
            </button>
            <div className="flex flex-col sm:flex-row items-start">
                <img src={`https://i.pravatar.cc/150?u=${activePolitician.id}`} alt={activePolitician.name} className="w-24 h-24 rounded-full mr-6 mb-4 sm:mb-0 border-4 border-gray-200"/>
                <div>
                    <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">{activePolitician.name}</h1>
                    <p className="text-lg text-gray-600 dark:text-gray-400"><strong>Party:</strong> {activePolitician.party}</p>
                    <p className="text-lg text-gray-600 dark:text-gray-400"><strong>Office:</strong> {activePolitician.office}</p>
                    <p className="text-lg text-gray-600 dark:text-gray-400"><strong>Term:</strong> {formatTermDates(activePolitician.term_start, activePolitician.term_end)}</p>
                </div>
            </div>
            <Timeline politician={activePolitician} events={mockTimelineEvents} />
          </div>
        ) : (
          // Search/Home View
          <div className="text-center">
            <header className="my-8 sm:my-12">
              <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white tracking-tight">Politi-Track</h1>
              <p className="mt-2 text-lg text-gray-500 dark:text-gray-400">Your source for political career tracking.</p>
            </header>
            <SearchBar onSearch={handleSearch} onResults={setSearchResults} onError={setError} />
            
            {isLoading && <div className="text-lg text-gray-500 dark:text-gray-400 mt-10">Loading...</div>}
            
            {error && <p className="text-red-500 mt-10">{error}</p>}
            
            {!isLoading && !error && searchResults.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 text-left mt-10">
                {searchResults.map((politician) => (
                  <div
                    key={politician.id}
                    className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-5 cursor-pointer hover:shadow-xl hover:scale-105 transition-all duration-200"
                    onClick={() => setActivePolitician(politician)}
                  >
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">{politician.name}</h3>
                    <p className="text-gray-600 dark:text-gray-400">{politician.party} - {politician.office}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">{formatTermDates(politician.term_start, politician.term_end)}</p>
                  </div>
                ))}
              </div>
            )}
            
            {!isLoading && !error && searchResults.length === 0 && searchQuery && (
              <p className="text-lg text-gray-500 dark:text-gray-400 mt-10">No results found for "{searchQuery}"</p>
            )}

            {!isLoading && !searchQuery && (
              <p className="text-lg text-gray-500 dark:text-gray-400 mt-10">Enter a name above to search for a politician.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
