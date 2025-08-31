# database.py
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "../politics.db")
db_abs_path = os.path.abspath(db_path)

engine = create_engine(f"sqlite:///{db_abs_path}", echo=True)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
