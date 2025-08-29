from datetime import date
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.sql import text
from models import Gift, Politician
import sqlite3
import os

# Remove existing database to ensure clean schema
if os.path.exists('politics.db'):
    os.remove('politics.db')

# Create engine and generate schema
engine = create_engine("sqlite:///politics.db")
SQLModel.metadata.create_all(engine)

# Enable foreign keys in SQLite
with engine.connect() as con:
    con.execute(text("PRAGMA foreign_keys = ON"))

print("Schema generated successfully")

# Connect directly to SQLite to inspect table structure
conn = sqlite3.connect('politics.db')
cursor = conn.cursor()

# Get table info for gifts table
cursor.execute("PRAGMA table_info(gifts)")
columns = cursor.fetchall()

print("\nGifts table schema:")
for col in columns:
    print(f"  {col}")

# Verify primary key and foreign key constraints
cursor.execute("PRAGMA foreign_key_list(gifts)")
fk_constraints = cursor.fetchall()

print("\nForeign key constraints:")
for fk in fk_constraints:
    print(f"  {fk}")

# Check if id is primary key
id_column = [col for col in columns if col[1] == 'id'][0]
assert id_column[5] == 1, "id column should be primary key"

# Verify politician_id has foreign key constraint
assert len(fk_constraints) > 0, "Should have foreign key constraint"
assert fk_constraints[0][3] == 'politician_id', "Foreign key should reference politician_id column"
assert fk_constraints[0][2] == 'politicians', "Foreign key should reference politicians table"
assert fk_constraints[0][4] == 'id', "Foreign key should reference politicians.id column"

print("\nSchema verification passed!")

# Test data insertion
