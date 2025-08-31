from datetime import date
from models import VoteRecord, Politician

# Create a sample Politician instance (required for foreign key relationship, though not strictly needed for pydantic validation)
politician = Politician(
    name="John Doe",
    party="Independent",
    office="Senator",
    term_start=date(2023, 1, 3),
    term_end=date(2029, 1, 3)
)

# Instantiate a VoteRecord with sample data
record = VoteRecord(
    politician_id=1,
    bill_name="Infrastructure Bill 2023",
    bill_status="Passed",
    vote_outcome="Yes",
    session_year=2023
)

# Print the object to verify attributes
print("VoteRecord object created successfully:")
print(record)

# Confirm no validation error occurred
print("\nAll attributes are correctly set.")
