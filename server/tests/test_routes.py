import pytest
from fastapi.testclient import TestClient
from server.main import app
from unittest.mock import patch
from sqlmodel import Session
from server.database import engine

# Create test client for FastAPI app
client = TestClient(app)

def test_search_by_politician_name():
    """Test searching by politician name"""
    # This test will make a request assuming the database is populated
    response = client.get("/search", params={"q": "Alexandria"})
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    results = data["results"]
    
    # Should return at least one result for Alexandria Ocasio-Cortez
    assert len(results) > 0
    
    # Find AOC in results
    aoc_results = [p for p in results if "Alexandria" in p["name"]]
    assert len(aoc_results) > 0
    
    # Verify required fields are present
    politician = aoc_results[0]
    required_fields = ["id", "name", "party", "office", "term_start", "term_end"]
    for field in required_fields:
        assert field in politician

def test_search_by_bill_details():
    """Test searching by bill details (e.g., infrastructure)"""
    response = client.get("/search", params={"q": "infrastructure"})
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    results = data["results"]
    
    # Results should include relevant politicians
    assert isinstance(results, list)
    
    # Verify structure of non-empty responses
    if len(results) > 0:
        required_fields = ["id", "name", "party", "office", "term_start", "term_end"]
        for politician in results:
            for field in required_fields:
                assert field in politician

def test_search_by_gift_description():
    """Test searching by gift description (e.g., conference)"""
    response = client.get("/search", params={"q": "conference"})
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    results = data["results"]
    
    # Results should include relevant politicians
    assert isinstance(results, list)
    
    # Verify structure of non-empty responses
    if len(results) > 0:
        required_fields = ["id", "name", "party", "office", "term_start", "term_end"]
        for politician in results:
            assert all(field in politician for field in required_fields)

def test_search_no_results():
    """Test searching with a term that should return no results"""
    # Use a unique string not likely to appear in any data
    response = client.get("/search", params={"q": "xyzrandomuniquestring"})
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert data["results"] == []

@patch("server.api.routes.search_politicians")
def test_search_database_error(mock_search):
    """Test handling of database connection errors"""
    # Simulate a database error
    mock_search.side_effect = Exception("Database connection failed")
    
    response = client.get("/search", params={"q": "Alexandria"})
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Internal server error" in data["detail"]

def test_search_input_validation():
    """Test input validation for the search parameter"""
    # Test empty query
    response = client.get("/search", params={"q": ""})
    assert response.status_code == 422  # Unprocessable Entity
    
    # Test very long query
    long_query = "a" * 101
    response = client.get("/search", params={"q": long_query})
    assert response.status_code == 422  # Unprocessable Entity
    
    # Test special characters (only alphanumeric, spaces, hyphens, and apostrophes allowed)
    response = client.get("/search", params={"q": "test!"})
    assert response.status_code == 422  # Unprocessable Entity

    # Test hyphenated name (should be accepted)
    response = client.get("/search", params={"q": "Ocasio-Cortez"})
    assert response.status_code == 200

    # Test name with apostrophe (should be accepted)
    response = client.get("/search", params={"q": "O'Connor"})
    assert response.status_code == 200
