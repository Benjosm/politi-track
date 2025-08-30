import React, { useState } from 'react';
import { Politician } from '../lib/types';

interface SearchBarProps {
  onSearch: (query: string) => void;
  onResults: (results: Politician[]) => void;
  onError: (error: string | null) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, onResults, onError }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    onSearch(query.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search politicians..."
        data-testid="search-input"
      />
      <button type="submit" disabled={!query.trim()}>
        Search
      </button>
    </form>
  );
};

export default SearchBar;
