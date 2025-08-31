from fastapi import APIRouter, Query, Depends, HTTPException
from sqlmodel import Session, select, or_, func, col
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timedelta
import math

# --- Import all the new, enhanced models ---
from server.models import (
    Politician, 
    PoliticalPosition, 
    PartyAffiliation, 
    Vote, 
    Bill, 
    Gift, 
    CommitteeMembership, 
    Committee,
    CampaignDonation,
    FinancialDisclosure,
    Source
)
from server.database import get_session

router = APIRouter()

# --- Models for the /search endpoint ---

class PoliticianSearchResult(SQLModel):
    """A concise summary of a politician for search results."""
    id: int
    full_name: str
    current_party: Optional[str] = None
    current_position_title: Optional[str] = None
    jurisdiction: Optional[str] = None

class SearchResponse(SQLModel):
    results: List[PoliticianSearchResult]

# --- Models for the GET /politicians endpoint (List View) ---

class PoliticianSortBy(str, Enum):
    """Fields available for sorting the list of politicians."""
    LAST_NAME_ASC = "last_name_asc"
    LAST_NAME_DESC = "last_name_desc"
    FIRST_NAME_ASC = "first_name_asc"
    FIRST_NAME_DESC = "first_name_desc"

class PaginatedPoliticianResponse(SQLModel):
    """Wrapper model for returning a paginated list of politicians."""
    total: int
    page: int
    size: int
    pages: int
    results: List[PoliticianSearchResult]


# --- Models for Create/Update Endpoints ---

class PoliticianCreate(SQLModel):
    """Data needed to create a new Politician."""
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    biography: Optional[str] = None
    official_website_url: Optional[str] = None
    source_id: Optional[int] = None # Optional foreign key

class PoliticianUpdate(SQLModel):
    """Data that can be provided to update a Politician. All fields are optional."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    biography: Optional[str] = None
    official_website_url: Optional[str] = None
    source_id: Optional[int] = None

class PoliticianPublic(PoliticianCreate):
    """Public representation of a Politician, including the ID."""
    id: int

# --- Models for the /politicians/{id} endpoint (full details) ---

class SourcePublic(SQLModel):
    name: str
    url: Optional[str]
    retrieval_date: str

class PoliticalPositionPublic(SQLModel):
    title: str
    jurisdiction: str
    start_date: str
    end_date: Optional[str]
    is_current: bool

class PartyAffiliationPublic(SQLModel):
    party_name: str
    start_date: str
    end_date: Optional[str]

class VotePublic(SQLModel):
    vote_date: str
    position: str
    bill_number: str
    bill_title: str

class GiftPublic(SQLModel):
    description: str
    value: float
    report_date: str
    donor: str

class CampaignDonationPublic(SQLModel):
    """Public representation of a single financial donation."""
    donor_name: str
    donor_type: str
    amount: float
    date: str # Converted from date type

class FinancialDisclosurePublic(SQLModel):
    """Public representation of a filed financial disclosure report."""
    report_year: int
    filing_date: str # Converted from date type
    document_url: str
    # Note: If you stored assets/liabilities, they would be nested here.

class CommitteeDetailPublic(SQLModel):
    """Nested detail model for the Committee object."""
    name: str
    chamber: str

class CommitteeMembershipPublic(SQLModel):
    """Represents the politician's specific role and term on a committee."""
    role: str
    start_date: str
    end_date: Optional[str]
    committee: CommitteeDetailPublic # Nested details of the committee itself

class PoliticianFullDetails(SQLModel):
    """The complete, detailed public profile of a politician."""
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[str] = None
    biography: Optional[str] = None
    official_website_url: Optional[str] = None
    
    # Auditing/Source Information for the primary record
    source: Optional[SourcePublic] = None 
    
    # Normalized Career History
    positions: List[PoliticalPositionPublic]
    party_affiliations: List[PartyAffiliationPublic]
    committee_memberships: List[CommitteeMembershipPublic]
    
    # Legislative Activity
    votes: List[VotePublic]
    
    # Financial and Ethics Data
    gifts_received: List[GiftPublic]
    campaign_donations: List[CampaignDonationPublic]
    financial_disclosures: List[FinancialDisclosurePublic]
    
    # Add other public links
    # social_media_accounts: List[SocialMediaAccountPublic] # (If defined)

@router.get("/health/db")
def test_db_session(db: Session = Depends(get_session)):
    """Health check endpoint to verify database session injection."""
    try:
        db.scalar(select(1))
        return {"status": "connected", "database": "reachable"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9 \\'-.]{1,100}$", description="Alphanumeric search term"),
    db: Session = Depends(get_session)
):
    """
    Search for politicians by name, bill titles they voted on, or committees they serve on.
    """
    try:
        search_term = f"%{q.lower()}%" # Prepare for LIKE query

        # This query is more complex as it searches across multiple relationships
        query = (
            select(Politician)
            .distinct()
            .where(
                or_(
                    # Search by first, last, or full name
                    func.lower(Politician.first_name).like(search_term),
                    func.lower(Politician.last_name).like(search_term),
                    func.lower(Politician.first_name + ' ' + Politician.last_name).like(search_term),
                    
                    # Search by the title of bills they voted on
                    Politician.votes.any(
                        Vote.bill.has(func.lower(Bill.title).like(search_term))
                    ),
                    
                    # Search by the name of committees they are a member of
                    Politician.committee_memberships.any(
                        CommitteeMembership.committee.has(func.lower(Committee.name).like(search_term))
                    )
                )
            )
            # Eagerly load the relationships needed for the summary view
            .options(
                selectinload(Politician.positions),
                selectinload(Politician.party_affiliations)
            )
            .order_by(Politician.last_name)
        )
        
        politicians = db.exec(query).all()
        
        # Process results into the Pydantic response model
        results_list = []
        for p in politicians:
            current_pos = next((pos for pos in p.positions if pos.is_current), None)
            current_party = next((party for party in p.party_affiliations if party.end_date is None), None)

            results_list.append(
                PoliticianSearchResult(
                    id=p.id,
                    full_name=f"{p.first_name} {p.last_name}",
                    current_party=current_party.party_name if current_party else "N/A",
                    current_position_title=current_pos.title if current_pos else "N/A",
                    jurisdiction=current_pos.jurisdiction if current_pos else "N/A"
                )
            )

        return SearchResponse(results=results_list)

    except Exception as e:
        print(f"Search Error: {e}") # For debugging
        raise HTTPException(status_code=500, detail="Internal server error occurred during search.")

@router.get("/politicians", response_model=PaginatedPoliticianResponse)
async def get_politicians(
    db: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    sort_by: Optional[PoliticianSortBy] = Query(PoliticianSortBy.LAST_NAME_ASC, description="Sort order"),
    party: Optional[str] = Query(None, description="Filter by current political party (case-insensitive)"),
    jurisdiction: Optional[str] = Query(None, description="Filter by current jurisdiction (case-insensitive)")
):
    """
    Get a paginated list of politicians, with options for sorting and filtering.
    """
    base_query = select(Politician)
    
    # Apply filters by joining to related tables
    if party:
        base_query = base_query.join(PartyAffiliation).where(
            func.lower(PartyAffiliation.party_name) == party.lower(), 
            PartyAffiliation.end_date == None
        ).distinct()

    if jurisdiction:
        base_query = base_query.join(PoliticalPosition).where(
            func.lower(PoliticalPosition.jurisdiction) == jurisdiction.lower(),
            PoliticalPosition.is_current == True
        ).distinct()

    # Get total count for pagination metadata, using the filtered query as a subquery
    count_query = select(func.count()).select_from(base_query.subquery())
    total_count = db.exec(count_query).one()

    # Apply sorting
    if sort_by == PoliticianSortBy.LAST_NAME_ASC:
        order_clause = col(Politician.last_name).asc()
    elif sort_by == PoliticianSortBy.LAST_NAME_DESC:
        order_clause = col(Politician.last_name).desc()
    elif sort_by == PoliticianSortBy.FIRST_NAME_ASC:
        order_clause = col(Politician.first_name).asc()
    else: # PoliticianSortBy.FIRST_NAME_DESC
        order_clause = col(Politician.first_name).desc()

    # Apply pagination and eager loading
    offset = (page - 1) * size
    paginated_query = base_query.order_by(order_clause).offset(offset).limit(size).options(
        selectinload(Politician.positions),
        selectinload(Politician.party_affiliations)
    )
    
    politicians = db.exec(paginated_query).all()
    
    # Process results into the summary response model
    results_list = [
        PoliticianSearchResult(
            id=p.id,
            full_name=f"{p.first_name} {p.last_name}",
            current_party=next((pa.party_name for pa in p.party_affiliations if pa.end_date is None), "N/A"),
            current_position_title=next((pos.title for pos in p.positions if pos.is_current), "N/A"),
            jurisdiction=next((pos.jurisdiction for pos in p.positions if pos.is_current), "N/A")
        ) for p in politicians
    ]

    return PaginatedPoliticianResponse(
        total=total_count,
        page=page,
        size=size,
        pages=math.ceil(total_count / size) if total_count > 0 else 0,
        results=results_list
    )


@router.post("/politicians", response_model=PoliticianPublic, status_code=201)
async def create_politician(
    politician_data: PoliticianCreate,
    db: Session = Depends(get_session)
):
    """
    Create a new politician record.
    """
    # Check if a politician with the same name and DOB already exists to prevent duplicates
    query = select(Politician).where(
        Politician.first_name == politician_data.first_name,
        Politician.last_name == politician_data.last_name,
        Politician.date_of_birth == politician_data.date_of_birth
    )
    if db.exec(query).first():
        raise HTTPException(
            status_code=409, # Conflict
            detail="A politician with this name and date of birth already exists."
        )

    db_politician = Politician.model_validate(politician_data)
    db.add(db_politician)
    db.commit()
    db.refresh(db_politician)
    return db_politician


@router.patch("/politicians/{politician_id}", response_model=PoliticianPublic)
async def update_politician(
    politician_id: int,
    politician_update_data: PoliticianUpdate,
    db: Session = Depends(get_session)
):
    """
    Update a politician's record. Only provide the fields you want to change.
    """
    db_politician = db.get(Politician, politician_id)
    if not db_politician:
        raise HTTPException(status_code=404, detail="Politician not found")

    update_data = politician_update_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    for key, value in update_data.items():
        setattr(db_politician, key, value)
    
    db.add(db_politician)
    db.commit()
    db.refresh(db_politician)
    return db_politician

@router.get("/politicians/{politician_id}", response_model=PoliticianFullDetails)
async def get_politician_details(politician_id: int, db: Session = Depends(get_session)):
    """
    Retrieve the full, detailed record for a single politician by their ID.
    """
    # Use selectinload to eagerly load related data and avoid the N+1 query problem.
    # This fetches the politician and all related items in a few efficient queries.
    query = (
        select(Politician)
        .where(col(Politician.id) == politician_id)
        .options(
            selectinload(Politician.source),
            selectinload(Politician.positions),
            selectinload(Politician.party_affiliations),
            selectinload(Politician.gifts_received).selectinload(Gift.source),
            selectinload(Politician.votes).selectinload(Vote.bill),
            selectinload(Politician.committee_memberships).selectinload(CommitteeMembership.committee),
            selectinload(Politician.campaign_donations),
            selectinload(Politician.financial_disclosures),
        )
    )
    
    politician = db.exec(query).first()
    
    if not politician:
        raise HTTPException(status_code=404, detail="Politician not found")

    # Manually construct the detailed response model. This gives us full control
    # over formatting (like converting dates to strings).
    response_data = PoliticianFullDetails(
        # --- Basic Information ---
        id=politician.id,
        first_name=politician.first_name,
        last_name=politician.last_name,
        date_of_birth=politician.date_of_birth.isoformat() if politician.date_of_birth else None,
        biography=politician.biography,
        official_website_url=politician.official_website_url,
        
        # --- Auditing/Source Information ---
        source=SourcePublic(
            name=politician.source.name,
            url=politician.source.url,
            retrieval_date=politician.source.retrieval_date.isoformat()
        ) if politician.source else None,

        # --- Career History ---
        positions=[
            PoliticalPositionPublic(
                title=pos.title,
                jurisdiction=pos.jurisdiction,
                start_date=pos.start_date.isoformat(),
                end_date=pos.end_date.isoformat() if pos.end_date else None,
                is_current=pos.is_current
            ) for pos in sorted(politician.positions, key=lambda x: x.start_date, reverse=True)
        ],
        party_affiliations=[
            PartyAffiliationPublic(
                party_name=pa.party_name,
                start_date=pa.start_date.isoformat(),
                end_date=pa.end_date.isoformat() if pa.end_date else None
            ) for pa in sorted(politician.party_affiliations, key=lambda x: x.start_date, reverse=True)
        ],
        
        # --- Legislative Activity ---
        committee_memberships=[
            CommitteeMembershipPublic(
                role=cm.role,
                start_date=cm.start_date.isoformat(),
                end_date=cm.end_date.isoformat() if cm.end_date else None,
                committee=CommitteeDetailPublic(
                    name=cm.committee.name,
                    chamber=cm.committee.chamber.value
                )
            ) for cm in sorted(politician.committee_memberships, key=lambda x: x.start_date, reverse=True)
        ],
        votes=[
            VotePublic(
                vote_date=v.vote_date.isoformat(),
                position=v.position.value, # Access enum value
                bill_number=v.bill.bill_number,
                bill_title=v.bill.title
            ) for v in sorted(politician.votes, key=lambda x: x.vote_date, reverse=True)
        ],

        # --- Financial and Ethics Data ---
        gifts_received=[
            GiftPublic(
                description=g.description,
                value=g.value,
                report_date=g.report_date.isoformat(),
                donor=g.donor
            ) for g in sorted(politician.gifts_received, key=lambda x: x.report_date, reverse=True)
        ],
        campaign_donations=[
            CampaignDonationPublic(
                donor_name=cd.donor_name,
                donor_type=cd.donor_type,
                amount=cd.amount,
                date=cd.date.isoformat()
            ) for cd in sorted(politician.campaign_donations, key=lambda x: x.date, reverse=True)
        ],
        financial_disclosures=[
            FinancialDisclosurePublic(
                report_year=fd.report_year,
                filing_date=fd.filing_date.isoformat(),
                document_url=fd.document_url
            ) for fd in sorted(politician.financial_disclosures, key=lambda x: x.filing_date, reverse=True)
        ]
    )

    return response_data

class DataIssue(SQLModel):
    """Describes a single data quality issue for a record."""
    field: str
    message: str

class PoliticianDataHealth(SQLModel):
    """Summary of data quality issues for a single politician."""
    id: int
    full_name: str
    jurisdiction: Optional[str]
    issues: List[DataIssue]

class DataHealthResponse(SQLModel):
    """The response model for the data health endpoint."""
    politicians_with_issues: List[PoliticianDataHealth]

@router.get("/management/data-health", response_model=DataHealthResponse, tags=["Management"])
async def get_data_health_report(
    db: Session = Depends(get_session)
):
    """
    Scans the database to find politicians with outdated or missing information.
    
    This endpoint is designed for internal database management to identify records
    that require updates.
    
    - **Outdated** is defined as records not updated within the last 365 days.
    - **Missing** refers to key fields that are empty/null or required related records
    that are not present.
    """
    OUTDATED_THRESHOLD_DAYS = 365
    cutoff_date = datetime.utcnow() - timedelta(days=OUTDATED_THRESHOLD_DAYS)
    
    # Eagerly load relationships to avoid N+1 query problems during the check loop
    query = (
        select(Politician)
        .options(
            selectinload(Politician.positions),
            selectinload(Politician.party_affiliations),
            selectinload(Politician.financial_disclosures)
        )
        .order_by(Politician.last_name, Politician.first_name) # For consistent ordering
    )
    politicians = db.exec(query).all()
    
    politicians_with_issues = []
    
    for p in politicians:
        issues = []
        
        # --- CHECK 1: Missing Core Information ---
        if not p.date_of_birth:
            issues.append(DataIssue(field="date_of_birth", message="Missing date of birth."))
        if not p.biography:
            issues.append(DataIssue(field="biography", message="Missing biography."))
        if not p.official_website_url:
            issues.append(DataIssue(field="official_website_url", message="Missing official website URL."))
            
        # --- CHECK 2: Missing or Incomplete Relational Information ---
        if not p.positions:
            issues.append(DataIssue(field="positions", message="No political positions on record."))
        elif not any(pos.is_current for pos in p.positions):
            issues.append(DataIssue(field="positions", message="No position is marked as 'current'."))
            
        if not p.party_affiliations:
            issues.append(DataIssue(field="party_affiliations", message="No party affiliations on record."))
        elif not any(pa.end_date is None for pa in p.party_affiliations):
            issues.append(DataIssue(field="party_affiliations", message="No current party affiliation found (all have an end_date)."))
            
        # --- CHECK 3: Outdated Record Checks ---
        if p.updated_at < cutoff_date:
            issues.append(DataIssue(
                field="updated_at",
                message=f"Core record is stale; last updated on {p.updated_at.date()}."
            ))
            
        if p.financial_disclosures:
            latest_disclosure = max(p.financial_disclosures, key=lambda fd: fd.filing_date, default=None)
            if latest_disclosure and latest_disclosure.filing_date < cutoff_date.date():
                issues.append(DataIssue(
                    field="financial_disclosures",
                    message=f"Latest financial disclosure is from {latest_disclosure.filing_date}, which is over a year old."
                ))
        else:
            issues.append(DataIssue(field="financial_disclosures", message="No financial disclosures on record."))

        # If any issues were found for this politician, add them to the results
        if issues:
            current_pos = next((pos for pos in p.positions if pos.is_current), None)
            jurisdiction = current_pos.jurisdiction if current_pos else "N/A"
            
            politicians_with_issues.append(
                PoliticianDataHealth(
                    id=p.id,
                    full_name=f"{p.first_name} {p.last_name}",
                    jurisdiction=jurisdiction,
                    issues=issues
                )
            )
            
    return DataHealthResponse(politicians_with_issues=politicians_with_issues)
