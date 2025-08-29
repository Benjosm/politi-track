import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from server.models import Politician

def test_politician_instantiation():
    # Test instantiating a Politician with valid values
    politician = Politician(
        name="John Doe",
        party="Democratic",
        office="Senator",
        term_start=date(2020, 1, 3),
        term_end=date(2026, 1, 3)
    )
    
    # Verify no validation errors occur
    assert politician.name == "John Doe"
    assert politician.party == "Democratic"
    assert politician.office == "Senator"
    assert politician.term_start == date(2020, 1, 3)
    assert politician.term_end == date(2026, 1, 3)
    
    # Verify that the id can be None during instantiation
    assert politician.id is None
    
    # Verify that the relationship fields initialize as empty collections
    assert hasattr(politician, 'vote_records')
    assert isinstance(politician.vote_records, list)
    assert len(politician.vote_records) == 0
    
    assert hasattr(politician, 'gifts')
    assert isinstance(politician.gifts, list)
    assert len(politician.gifts) == 0
    
    print("All tests passed! Politician model is working correctly.")

if __name__ == "__main__":
    test_politician_instantiation()
