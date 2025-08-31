import React, { useState, useEffect, useCallback } from 'react';
import { getPoliticianDetails, searchPoliticians, getPoliticians } from './lib/api';
import { PoliticianDetails, PoliticianSummary, GetPoliticiansParams, PoliticianSortBy } from './lib/types';
import PoliticianListView from './components/PoliticianListView'; // Updated import
import PoliticianDetailView from './components/PoliticianDetailView';

function App() {
  // State for politician lists
  const [politicianList, setPoliticianList] = useState<PoliticianSummary[]>([]);
  const [searchResults, setSearchResults] = useState<PoliticianSummary[]>([]);
  
  // State for views
  const [selectedPoliticianId, setSelectedPoliticianId] = useState<number | null>(null);
  const [politicianDetails, setPoliticianDetails] = useState<PoliticianDetails | null>(null);

  // State for fetching and filtering
  const [isSearching, setIsSearching] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // State for API parameters
  const [filters, setFilters] = useState<GetPoliticiansParams>({
    page: 1,
    size: 9, // 9 works well for a 3-column grid
    sortBy: 'last_name_asc',
    party: '',
    jurisdiction: '',
  });
  const [pagination, setPagination] = useState({
    totalPages: 0,
  });

  // Main function to fetch the paginated list of politicians
  const fetchPoliticianList = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getPoliticians(filters);
      setPoliticianList(response.results);
      setPagination({ totalPages: response.pages });
    } catch (err) {
      setError('Failed to fetch the list of politicians.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [filters]);

  // Fetch the list on initial load and when filters change
  useEffect(() => {
    if (!isSearching) {
      fetchPoliticianList();
    }
  }, [fetchPoliticianList, isSearching]);
  
  // Fetch details when a politician is selected
  useEffect(() => {
    if (!selectedPoliticianId) {
      setPoliticianDetails(null);
      return;
    }
    const fetchDetails = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const details = await getPoliticianDetails(selectedPoliticianId);
        if (details) setPoliticianDetails(details);
        else setError('Could not find details for the selected politician.');
      } catch (err) {
        setError('Failed to fetch politician details.');
      } finally {
        setIsLoading(false);
      }
    };
    fetchDetails();
  }, [selectedPoliticianId]);

  const handleSearch = async (query: string) => {
    if (!query) {
      setIsSearching(false);
      setSearchResults([]);
      // Trigger a refresh of the main list
      setFilters(prev => ({...prev})); 
      return;
    }
    setIsSearching(true);
    setIsLoading(true);
    setError(null);
    try {
      const results = await searchPoliticians(query);
      setSearchResults(results);
    } catch (err) {
      setError('Search failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (newFilters: { party?: string; jurisdiction?: string }) => {
    setFilters(prev => ({
      ...prev,
      ...newFilters,
      page: 1, // Reset to first page on filter change
    }));
  };

  const handleSortChange = (sortBy: PoliticianSortBy) => {
    setFilters(prev => ({ ...prev, sortBy, page: 1 }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  const handleSelectPolitician = (id: number) => {
    setSelectedPoliticianId(id);
  };
  
  const handleBack = () => {
    setSelectedPoliticianId(null);
  };

  const displayedPoliticians = isSearching ? searchResults : politicianList;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 font-sans text-gray-800 dark:text-gray-200 p-4 sm:p-8">
      <div className="container mx-auto max-w-5xl">
        {selectedPoliticianId && politicianDetails ? (
          <PoliticianDetailView 
            politician={politicianDetails} 
            onBack={handleBack} 
          />
        ) : (
          <PoliticianListView
            politicians={displayedPoliticians}
            onSearch={handleSearch}
            onFilterChange={handleFilterChange}
            onSortChange={handleSortChange}
            onSelectPolitician={handleSelectPolitician}
            isLoading={isLoading}
            error={error}
            isSearching={isSearching}
            pagination={{
              currentPage: filters.page || 1,
              totalPages: pagination.totalPages,
              onPageChange: handlePageChange,
            }}
          />
        )}
      </div>
    </div>
  );
}

export default App;
