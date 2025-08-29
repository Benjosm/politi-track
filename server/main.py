from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, create_engine
from server.api.routes import router
from server.models import Politician, VoteRecord, Gift

# Database setup
DATABASE_URL = "sqlite:///./politics.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create the FastAPI application
app = FastAPI(
    title="PolitiTrack API",
    description="Public database of politician careers and disclosures"
)

# Include the search router
app.include_router(router)

def create_db_and_tables():
    """Create database tables with WAL mode enabled"""
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
        conn.commit()
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    """Create database tables when the application starts"""
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
