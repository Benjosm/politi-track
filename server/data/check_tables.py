import sqlite3

def check_tables():
    # Connect to the database
    conn = sqlite3.connect('politics.db')
    cursor = conn.cursor()

    # Check what tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")

    # Get schema for politicians table
    cursor.execute("PRAGMA table_info(politicians)")
    print("\nPoliticians table schema:")
    for row in cursor.fetchall():
        print(row)

    # Get schema for vote_records table
    cursor.execute("PRAGMA table_info(vote_records)")
    print("\nVote_records table schema:")
    for row in cursor.fetchall():
        print(row)

    # Check sample data from politicians table
    cursor.execute("SELECT * FROM politicians LIMIT 2")
    print("\nSample politicians data:")
    for row in cursor.fetchall():
        print(row)

    # Check sample data from vote_records table
    cursor.execute("SELECT * FROM vote_records LIMIT 5")
    print("\nSample vote_records data:")
    for row in cursor.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    check_tables()
