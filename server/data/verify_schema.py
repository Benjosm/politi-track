import sqlite3

conn = sqlite3.connect('politics.db')
cursor = conn.cursor()

# Check the actual schema of vote_records
# Check the actual schema of politicians
cursor.execute("PRAGMA table_info(politicians)")
print("Politicians table columns:")
for row in cursor.fetchall():
    print(row)

# Check the actual schema of vote_records
cursor.execute("PRAGMA table_info(vote_records)")
print("\nVote_records table columns:")
for row in cursor.fetchall():
    print(row)

# Check the actual schema of gifts
cursor.execute("PRAGMA table_info(gifts)")
print("\nGifts table columns:")
for row in cursor.fetchall():
    print(row)

# Check foreign key constraints
cursor.execute("PRAGMA foreign_key_list(vote_records)")
print("\nVote_records foreign keys:")
for row in cursor.fetchall():
    print(row)

cursor.execute("PRAGMA foreign_key_list(gifts)")
print("\nGifts foreign keys:")
for row in cursor.fetchall():
    print(row)

# Check a few sample records to see actual data
cursor.execute("SELECT * FROM politicians LIMIT 2")
print("\nSample politicians:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM vote_records LIMIT 2")
print("\nSample vote records:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM gifts LIMIT 2")
print("\nSample gifts:")
for row in cursor.fetchall():
    print(row)

conn.close()
