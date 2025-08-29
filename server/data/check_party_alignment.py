import sqlite3
import random
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../politics.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get a sample politician
cursor.execute('SELECT id, party FROM politicians LIMIT 1')
result = cursor.fetchone()
if result is None:
    print("No politicians found in database")
    conn.close()
    exit()

politician_id, party = result

# Determine expected vote based on party
# In the seed script: Democrats tend toward "Yes", Republicans toward "No"
if party == "Democrat":
    expected_vote = "Yes"
elif party == "Republican":
    expected_vote = "No"
else: # Independent
    # From seed script: Independents have random but consistent expected vote
    # We'll assume 50/50 Yes/No which matches the seed script's approach
    expected_vote = random.choice(["Yes", "No"])

# Get votes from that politician (using correct column name 'vote_position')
cursor.execute('''
SELECT vote_position FROM vote_records 
WHERE politician_id = ? 
LIMIT 20
''', (politician_id,))
votes = [row[0] for row in cursor.fetchall()]

# Calculate alignment with expected vote
aligned_votes = sum(1 for vote in votes if vote == expected_vote)
total_votes = len(votes)
alignment_percentage = (aligned_votes / total_votes) * 100 if total_votes > 0 else 0

print(f"Sample politician ID: {politician_id}")
print(f"Party: {party}")
print(f"Expected vote: {expected_vote}")
print(f"Number of votes sampled: {total_votes}")
print(f"Votes aligned with expected vote: {aligned_votes}")
print(f"Alignment percentage: {alignment_percentage:.1f}%")
print(f"Votes: {votes}")

conn.close()
