from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import Table

# Connect to the database
engine = create_engine("sqlite:///politics.db")
inspector = inspect(engine)

# Get the list of tables
tables = inspector.get_table_names()
print("Tables in database:", tables)

# Check for vote_records table
if "vote_records" in tables:
    print("\nColumns in 'vote_records' table:")
    columns = inspector.get_columns("vote_records")
    for col in columns:
        print(f"  {col['name']}: {col['type']} (nullable: {col['nullable']}, primary_key: {col['primary_key']})")

    print("\nForeign keys in 'vote_records' table:")
    fks = inspector.get_foreign_keys("vote_records")
    for fk in fks:
        print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns'][0]}")
else:
    print("vote_records table does not exist!")

# Verify politicians table exists and has primary key
if "politicians" in tables:
    print("\n'politicians' table exists with primary key.")
else:
    print("\n'politicians' table does not exist!")
