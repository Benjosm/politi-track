from sqlmodel import SQLModel, create_engine
from server.models import Politician, VoteRecord, Gift

# Database setup
DATABASE_URL = "sqlite:///./politics.db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for SQL logging

def create_db_and_tables():
    # Enable WAL mode first
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
        conn.commit()
    # Create tables
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
