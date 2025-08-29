import sqlite3
import os
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../politics.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
SELECT politician_id, COUNT(*) 
FROM vote_records 
GROUP BY politician_id 
HAVING COUNT(*) < 10;
''')
results = cursor.fetchall()
print(f"Politicians with fewer than 10 votes: {len(results)}")
for row in results:
    print(row)
conn.close()
