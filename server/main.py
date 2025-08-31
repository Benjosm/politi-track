from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from server.database import engine, SQLModel
from server.models import Politician, VoteRecord, Gift

# Create the FastAPI application
app = FastAPI(
    title="PolitiTrack API",
    description="Public database of politician careers and disclosures"
)

# Allow your frontend origin
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
