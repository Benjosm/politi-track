from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from server.api.routes import router
from server.database import engine
from server.models import Politician, VoteRecord, Gift

# Create the FastAPI application
app = FastAPI(
    title="PolitiTrack API",
    description="Public database of politician careers and disclosures"
)

# Include the search router
app.include_router(router)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    """Create database tables when the application starts"""
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
