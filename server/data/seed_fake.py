from sqlmodel import Session, create_engine, SQLModel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from server.models import Politician, VoteRecord, Gift
from faker import Faker
import random
from datetime import date

def seed_db(session: Session):
    """
    Populate the database with fake politician data and associated vote records.
    
    Args:
        session: SQLAlchemy Session object
    """
    faker = Faker()
    
    # Political party and office choices
    parties = ["Republican", "Democrat", "Independent"]
    offices = ["Senator", "Representative", "Governor"]
    
    # Generate at least 5 politicians
    for _ in range(5):
        # Generate random dates for term start and end
        term_start = faker.date_between(start_date="-10y", end_date="today")
        # Ensure term end is at least 2 years after start, but no more than 6 years
        term_end = faker.date_between(start_date=term_start, end_date=f"+6y")
        
        # Create a new politician instance
        politician = Politician(
            name=faker.name(),
            party=random.choice(parties),
            office=random.choice(offices),
            term_start=term_start,
            term_end=term_end
        )
        
        # Add the politician to the session and commit to get its ID
        session.add(politician)
        session.commit()
        session.refresh(politician)
        
        # Create exactly 10+ VoteRecord instances for this politician
        num_votes = 11  # Exactly 11 vote records per politician (more than 10)
        party_affiliation = politician.party
        
        # Define party-based expected vote outcomes
        # For simplicity, assume Democrats tend to vote "Yes" and Republicans "No"
        # Independents will have a random preference that stays consistent
        party_expected_vote = {
            "Democrat": "Yes",
            "Republican": "No"
        }
        # For Independents, randomly choose their expected vote pattern
        if party_affiliation == "Independent":
            party_expected_vote["Independent"] = random.choice(["Yes", "No"])
            
        expected_outcome = party_expected_vote.get(party_affiliation, random.choice(["Yes", "No"]))
        
        for _ in range(num_votes):
            bill_name = faker.sentence(nb_words=4)
            bill_status = random.choice(["passed", "failed", "pending"])
            
            # Determine vote outcome based on 70% party correlation rule
            if random.random() < 0.7:  # 70% of the time, align with party
                vote_outcome = expected_outcome
            else:  # 30% of the time, diverge from party
                # Choose any outcome except the expected one
                all_outcomes = ["Yes", "No", "Abstain", "Absent"]
                all_outcomes.remove(expected_outcome)
                vote_outcome = random.choice(all_outcomes)
            
            vote_record = VoteRecord(
                politician_id=politician.id,
                bill_name=bill_name,
                bill_status=bill_status,
                vote_position=vote_outcome,
                session_year=random.randint(2010, 2023)
            )
            session.add(vote_record)
        
        # Commit the vote records
        session.commit()
        
        # Create 2–4 Gift instances for this politician
        num_gifts = random.randint(2, 4)
        for _ in range(num_gifts):
            gift = Gift(
                politician_id=politician.id,
                description=faker.text(max_nb_chars=100),
                value=random.uniform(50, 10000),
                report_date=faker.date_this_decade(),
                source=faker.company()
            )
            session.add(gift)
        
        # Commit the gifts
        session.commit()

if __name__ == "__main__":
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../politics.db'))
    engine = create_engine(f"sqlite:///{db_path}")
    # Drop all tables first to ensure clean schema
    SQLModel.metadata.drop_all(engine)
    # Then create all tables based on current models
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_db(session)
