import sqlite3

def check_tables():
    # Connect to the database
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Check what tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")

    conn.close()

if __name__ == "__main__":
    check_tables()
