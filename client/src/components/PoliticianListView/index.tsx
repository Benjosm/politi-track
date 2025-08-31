import React from 'react';
import { PoliticianSummary } from '../../lib/types';
import FilterControls from '../FilterControls';
import Pagination from '../Pagination';

interface PoliticianListViewProps {
  politicians: PoliticianSummary[];
  onSearch: (query: string) => void;
  onFilterChange: (filters: { party?: string; jurisdiction?: string }) => void;
  onSortChange: (sortBy: any) => void;
  onSelectPolitician: (id: number) => void;
  isLoading: boolean;
  error: string | null;
  pagination: {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
  };
  isSearching: boolean; // To differentiate between search results and filtered list
}

const PoliticianListView: React.FC<PoliticianListViewProps> = ({
  politicians,
  onSearch,
  onFilterChange,
  onSortChange,
  onSelectPolitician,
  isLoading,
  error,
  pagination,
  isSearching,
}) => {
  return (
    <div className="animate-fade-in">
      <header className="text-center my-8 sm:my-12">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white tracking-tight">Politi-Track</h1>
        <p className="mt-2 text-lg text-gray-500 dark:text-gray-400">Your source for political career tracking.</p>
      </header>
      
      <FilterControls 
        onSearch={onSearch}
        onFilterChange={onFilterChange}
        onSortChange={onSortChange}
      />
      
      {isLoading && <div className="text-lg text-center text-gray-500 dark:text-gray-400 mt-10">Loading...</div>}
      
      {error && <p className="text-red-500 text-center mt-10">{error}</p>}
      
      {!isLoading && !error && politicians.length > 0 && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 text-left mt-10">
            {politicians.map((p) => (
              <div
                key={p.id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-5 cursor-pointer hover:shadow-xl hover:scale-105 transition-all duration-200"
                onClick={() => onSelectPolitician(p.id)}
              >
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">{p.full_name}</h3>
                <p className="text-gray-600 dark:text-gray-400">{p.current_position_title || 'N/A'}</p>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">{p.jurisdiction || ''}</p>
              </div>
            ))}
          </div>
          {!isSearching && (
             <Pagination 
                currentPage={pagination.currentPage}
                totalPages={pagination.totalPages}
                onPageChange={pagination.onPageChange}
             />
          )}
        </>
      )}
      
      {!isLoading && !error && politicians.length === 0 && (
        <p className="text-lg text-center text-gray-500 dark:text-gray-400 mt-10">
          No politicians found matching your criteria.
        </p>
      )}
    </div>
  );
};

export default PoliticianListView;
