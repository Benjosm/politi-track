import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../politics.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check politician party name format
cursor.execute("SELECT id, party FROM politicians LIMIT 5")
print("Politician party names:")
for row in cursor.fetchall():
    print(row)

# Check vote records for politician ID 1
cursor.execute("SELECT * FROM vote_records WHERE politician_id = 1")
print("\nVote records for politician 1:")
for row in cursor.fetchall():
    print(row)

# Check the exact column names in vote_records
cursor.execute("PRAGMA table_info(vote_records)")
print("\nVote_records columns:")
for row in cursor.fetchall():
    print(row[1])  # Print just the column name

conn.close()
