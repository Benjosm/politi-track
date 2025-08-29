import sqlite3
import os
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../politics.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
SELECT * FROM vote_records 
WHERE politician_id NOT IN (SELECT id FROM politicians);
''')
results = cursor.fetchall()
print(f"Vote records with invalid politician_id: {len(results)}")
for row in results:
    print(row)
conn.close()
