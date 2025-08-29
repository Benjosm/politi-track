from sqlmodel import SQLModel, create_engine
from server.models import Politician, VoteRecord, Gift

# Database setup
DATABASE_URL = "sqlite:///politician.db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for SQL log output

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
