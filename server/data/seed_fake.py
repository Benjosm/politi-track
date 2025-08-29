from sqlmodel import Session, create_engine, SQLModel, select
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
        
        # Create exactly 11 VoteRecord instances for this politician
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
    
    # Retrieve all existing politicians before seeding gifts
    politicians = session.exec(select(Politician)).all()
    if not politicians:
        raise ValueError("No politicians found in database. Gift seeding requires existing politician records.")
    
    # Define mapping of voting keywords to related industries for gift sources
    keyword_to_industry = {
        "energy": ["ExxonMobil", "Chevron", "Shell", "BP", "ConocoPhillips"],
        "environment": ["NextEra Energy", "Vestas", "First Solar", "Orsted", "Siemens Gamesa"],
        "health": ["Johnson & Johnson", "Pfizer", "Merck", "AbbVie", "Amgen"],
        "defense": ["Lockheed Martin", "Raytheon", "Boeing Defense", "Northrop Grumman", "General Dynamics"],
        "technology": ["Google", "Microsoft", "Amazon", "Meta", "Apple"],
        "finance": ["JPMorgan Chase", "Goldman Sachs", "Morgan Stanley", "Citigroup", "Bank of America"],
        "agriculture": ["Cargill", "Archer Daniels Midland", "Pilgrim's Pride", "Tyson Foods", "Land O'Lakes"],
        "transportation": ["Union Pacific", "FedEx", "United Airlines", "Delta Air Lines", "Caterpillar"]
    }
    
    # Create gifts for all politicians
    for politician in politicians:
        # Get all vote records for this politician to analyze voting patterns
        vote_records = session.exec(select(VoteRecord).where(VoteRecord.politician_id == politician.id)).all()
        
        # Extract keywords from bill names to determine likely gift sources
        politician_keywords = []
        for vote in vote_records:
            bill_name_lower = vote.bill_name.lower()
            for keyword in keyword_to_industry.keys():
                if keyword in bill_name_lower:
                    politician_keywords.append(keyword)
        
        # If no keywords found, use a default industry
        if not politician_keywords:
            politician_keywords = ["finance"]  # Default industry for politicians with no clear pattern
        
        # Generate at least 5 gift records per politician
        for _ in range(6):  # Increased to 6 to ensure "5+" gifts per politician
            # Select a random keyword from the politician's voting pattern
            keyword = random.choice(politician_keywords)
            # Select a random company from the corresponding industry
            source = random.choice(keyword_to_industry[keyword])
            
            # Generate gift value using log-normal distribution (keeps values realistic between ~$100-$50,000)
            value = round(random.lognormvariate(8.5, 0.8), 2)
            
            gift = Gift(
                politician_id=politician.id,
                description=faker.text(max_nb_chars=200),
                value=value,
                report_date=faker.date_this_year(),
                source=source  # Now using source from industry mapping, not faker
            )
            session.add(gift)
        
        # Commit gifts in batches per politician
        session.commit()

def run_seed():
    """
    Entrypoint for running the seed script via `poetry run seed-db`.
    Drops existing tables, recreates schema, and populates with fake data.
    """
    from server.database import engine
    # Drop all tables first to ensure clean schema
    SQLModel.metadata.drop_all(engine)
    # Then create all tables based on current models
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_db(session)
        session.commit()  # Ensure final commit
    # Explicitly dispose of the engine to close all connections
    engine.dispose()

if __name__ == "__main__":
    run_seed()

# Entry point for poetry scripts
seed_db_from_script = run_seed
