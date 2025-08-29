from fastapi import APIRouter, Query, Depends, HTTPException
from sqlmodel import Session, select, or_, func
from typing import List
from server.models import Politician, VoteRecord, Gift
from server.database import get_session

router = APIRouter()


@router.get("/health/db")
def test_db_session(db: Session = Depends(get_session)):
    """
    Health check endpoint to verify database session injection.
    Attempts to execute a simple query to confirm connectivity.
    """
    try:
        # Execute a minimal query to check database connectivity
        db.scalar(select(1))
        return {"status": "connected", "database": "reachable"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")



async def search_politicians(db: Session, q: str) -> List[dict]:
    """
    Search politicians by name, bill details, or gift descriptions.
    Returns distinct politicians matching the query.
    """
    try:
        # Convert search query to lowercase for case-insensitive matching
        search_term = q.lower()
        
        # Build a query to find politicians with matching name, bill details, or gift descriptions
        # Use distinct() to ensure no duplicate politicians are returned
        query = (
            select(Politician)
            .distinct()
            .where(
                or_(
                    func.lower(Politician.name).contains(search_term),
                    Politician.vote_records.any(or_(
                        func.lower(VoteRecord.bill_name).contains(search_term),
                        func.lower(VoteRecord.bill_status).contains(search_term)
                    )),
                    Politician.gifts.any(func.lower(Gift.description).contains(search_term))
                )
            )
            .order_by(Politician.name)
        )
        
        # Execute the query
        results = db.exec(query).all()
        
        # Project results to include only the required fields
        return [
            {
                "id": politician.id,
                "name": politician.name,
                "party": politician.party,
                "office": politician.office,
                "term_start": politician.term_start.isoformat() if politician.term_start else None,
                "term_end": politician.term_end.isoformat() if politician.term_end else None
            }
            for politician in results
        ]
        
    except Exception as e:
        # Re-raise the exception to be handled by the endpoint
        raise e

@router.get("/search")
async def search(
    q: str = Query(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9 \\'-.]{1,100}$", description="Alphanumeric search term with hyphens and apostrophes (1-1,00 chars)"),
    db: Session = Depends(get_session)
):
    """
    Search endpoint for politician data.
    Validates input and attempts to query the database.
    Returns empty results if no match or feature not implemented.
    """
    try:
        results = await search_politicians(db, q)
        return {"results": results}
    except Exception as e:
        # Return 500 Internal Server Error for database connection errors
        raise HTTPException(status_code=500, detail="Internal server error occurred while processing your request.")
