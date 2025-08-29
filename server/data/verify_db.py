import sqlite3

def verify_database():
    # Connect to the database
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Check politicians table
    cursor.execute("SELECT COUNT(*) FROM politicians")
    politician_count = cursor.fetchone()[0]
    print(f"Number of politicians: {politician_count}")
    
    # Check vote_records table
    cursor.execute("SELECT COUNT(*), politician_id FROM vote_records GROUP BY politician_id")
    vote_records = cursor.fetchall()
    print(f"Vote records per politician: {vote_records}")
    
    # Check gifts table
    cursor.execute("SELECT COUNT(*), politician_id FROM gifts GROUP BY politician_id")
    gifts = cursor.fetchall()
    print(f"Gifts per politician: {gifts}")

    # Close connection
    conn.close()

if __name__ == "__main__":
    verify_database()
