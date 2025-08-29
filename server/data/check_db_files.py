import os
import sqlite3

# Check what database files exist
print("Database files in current directory:")
for file in os.listdir('.'):
    if file.endswith('.db'):
        size = os.path.getsize(file)
        print(f"  {file}: {size} bytes")

# Check what tables are in politics.db
if os.path.exists('politics.db'):
    conn = sqlite3.connect('politics.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nTables in politics.db: {tables}")
    conn.close()

# Check what tables are in test.db
if os.path.exists('test.db'):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nTables in test.db: {tables}")
    conn.close()
