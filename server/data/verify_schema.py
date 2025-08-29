import sqlite3

conn = sqlite3.connect('politics.db')
cursor = conn.cursor()

# Check the actual schema of vote_records
cursor.execute("PRAGMA table_info(vote_records)")
print("Vote_records table columns:")
for row in cursor.fetchall():
    print(row)

# Check a few sample vote records to see actual data
cursor.execute("SELECT * FROM vote_records LIMIT 5")
print("\nSample vote records:")
for row in cursor.fetchall():
    print(row)

conn.close()
