import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import { searchPoliticians } from './lib/api';
import React from 'react';

// Mock the API module
jest.mock('./lib/api');

describe('App Component', () => {
  const mockPoliticians = [
    {
      id: 1,
      name: 'Alexandria Ocasio-Cortez',
      party: 'Democratic',
      office: 'US House of Representatives',
      term_start: '2019-01-03',
      term_end: '2025-01-03'
    },
    {
      id: 2,
      name: 'Alexandria Jones',
      party: 'Independent',
      office: 'State Senate',
      term_start: '2020-01-01',
      term_end: '2024-12-31'
    },
    {
      id: 3,
      name: 'Alexandria Brown',
      party: 'Republican',
      office: 'City Council',
      term_start: '2018-01-01',
      term_end: '2022-12-31'
    }
  ];

  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
  });

  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText('PolitiTrack')).toBeInTheDocument();
  });

  test('displays loading state and then search results', async () => {
    // Mock a successful API response
    searchPoliticians.mockResolvedValue(mockPoliticians);

    render(<App />);

    // Simulate user typing and submitting a search
    const searchInput = screen.getByPlaceholderText('Search politicians...');
    fireEvent.change(searchInput, { target: { value: 'Alexandria' } });
    fireEvent.submit(screen.getByRole('form'));

    // Loading state should appear
    expect(screen.getByText('Loading...')).toBeInTheDocument();

    // Wait for results and verify
    await waitFor(() => {
      expect(screen.getByText('Alexandria Ocasio-Cortez')).toBeInTheDocument();
    });
    expect(screen.getAllByRole('listitem')).toHaveLength(3);
  });

  test('displays error message on API failure', async () => {
    // Mock a rejected API call
    searchPoliticians.mockRejectedValue(new Error('API Error'));

    render(<App />);

    // Simulate user search
    const searchInput = screen.getByPlaceholderText('Search politicians...');
    fireEvent.change(searchInput, { target: { value: 'Alexandria' } });
    fireEvent.submit(screen.getByRole('form'));

    // Wait for error state
    await waitFor(() => {
      expect(screen.getByText('Failed to search politicians. Please try again later.')).toBeInTheDocument();
    });
    expect(console.error).toHaveBeenCalled(); // Assuming console.error is called in handleSearch
  });
});
