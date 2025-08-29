import React, { useState } from 'react';

const SearchBar = ({ onSearch, onResults, onError }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
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
