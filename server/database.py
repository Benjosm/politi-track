from typing import Generator
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, Session
from .models import SQLModel

# Create engine with SQLite database
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "../politics.db")
db_abs_path = os.path.abspath(db_path)
print(f"Database absolute path: {db_abs_path}")
print(f"Database file exists before engine creation: {os.path.exists(db_abs_path)}")
engine = create_engine(f"sqlite:///{db_abs_path}", echo=True)  # Set echo=True to see SQL
print(f"Engine created with URL: {engine.url}")

# Set PRAGMA journal_mode=WAL for better concurrency
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency function that yields a database session.
    Ensures the session is properly closed after use.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
