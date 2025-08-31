import React from 'react';
import { PoliticianSortBy } from '../lib/types';

interface FilterControlsProps {
  onSearch: (query: string) => void;
  onFilterChange: (filters: { party?: string; jurisdiction?: string }) => void;
  onSortChange: (sortBy: PoliticianSortBy) => void;
}

// A simple debounce hook to prevent API calls on every keystroke
const useDebouncedCallback = (callback: (...args: any[]) => void, delay: number) => {
  const timeoutRef = React.useRef<NodeJS.Timeout | null>(null);
  return (...args: any[]) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = setTimeout(() => {
      callback(...args);
    }, delay);
  };
};

const FilterControls: React.FC<FilterControlsProps> = ({ onSearch, onFilterChange, onSortChange }) => {
  const [partyFilter, setPartyFilter] = React.useState('');
  const [jurisdictionFilter, setJurisdictionFilter] = React.useState('');
  const [searchQuery, setSearchQuery] = React.useState('');

  const debouncedFilterChange = useDebouncedCallback(onFilterChange, 500);

  const handlePartyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setPartyFilter(value);
    debouncedFilterChange({ party: value, jurisdiction: jurisdictionFilter });
  };
  
  const handleJurisdictionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setJurisdictionFilter(value);
    debouncedFilterChange({ party: partyFilter, jurisdiction: value });
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(searchQuery);
  }

  return (
    <div className="space-y-4 mb-8">
       <form onSubmit={handleSearchSubmit} className="w-full">
        <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Global search by name, bill, or committee..."
            className="w-full p-3 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />
       </form>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          type="text"
          value={partyFilter}
          onChange={handlePartyChange}
          placeholder="Filter by Party..."
          className="p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
        />
        <input
          type="text"
          value={jurisdictionFilter}
          onChange={handleJurisdictionChange}
          placeholder="Filter by Jurisdiction..."
          className="p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
        />
        <select 
          onChange={(e) => onSortChange(e.target.value as PoliticianSortBy)}
          className="p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
        >
          <option value="last_name_asc">Sort by Last Name (A-Z)</option>
          <option value="last_name_desc">Sort by Last Name (Z-A)</option>
          <option value="first_name_asc">Sort by First Name (A-Z)</option>
          <option value="first_name_desc">Sort by First Name (Z-A)</option>
        </select>
      </div>
    </div>
  );
};

export default FilterControls;
