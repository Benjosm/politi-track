from sqlmodel import Session, create_engine, SQLModel
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
        
        # Create 3-5 VoteRecord instances for this politician
        num_votes = random.randint(3, 5)
        for _ in range(num_votes):
            vote_record = VoteRecord(
                politician_id=politician.id,
                bill_name=faker.sentence(nb_words=4),
                bill_status=random.choice(["Passed", "Failed", "In Progress"]),
                vote_outcome=random.choice(["Yes", "No", "Abstain", "Absent"]),
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
    engine = create_engine("sqlite:///./test.db")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_db(session)
