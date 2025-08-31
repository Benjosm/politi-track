from typing import List, Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

# Using an Enum for fixed choices is good practice
class VotePosition(str, Enum):
    YES = "Yes"
    NO = "No"
    ABSTAIN = "Abstain"
    NOT_VOTING = "Not Voting"

class Chamber(str, Enum):
    HOUSE = "House"
    SENATE = "Senate"
    JOINT = "Joint"

# --- Core Auditing and Sourcing ---

class Source(SQLModel, table=True):
    """Stores the source of the data (e.g., an API, a website, a document)."""
    __tablename__ = "sources"
    
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "ProPublica Congress API", "FEC Bulk Data"
    url: Optional[str] = None      # URL for the API endpoint or webpage where data was found
    retrieval_date: datetime = Field(default_f=datetime.utcnow)
    description: Optional[str] = None

class AuditableBase(SQLModel):
    """A base model to add auditing fields to other models."""
    created_at: datetime = Field(default_f=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_f=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}, nullable=False)
    
    source_id: Optional[int] = Field(default=None, foreign_key="sources.id")
    source: Optional[Source] = Relationship()

class Politician(AuditableBase, table=True):
    """Core, relatively static information about a public servant."""
    __tablename__ = "politicians"
    
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    suffix: Optional[str] = None
    
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    biography: Optional[str] = None
    official_website_url: Optional[str] = None
    
    # --- Relationships to dynamic career info ---
    positions: List["PoliticalPosition"] = Relationship(back_populates="politician")
    party_affiliations: List["PartyAffiliation"] = Relationship(back_populates="politician")
    committee_memberships: List["CommitteeMembership"] = Relationship(back_populates="politician")
    votes: List["Vote"] = Relationship(back_populates="politician")
    sponsored_bills: List["Bill"] = Relationship(back_populates="sponsor")
    gifts_received: List["Gift"] = Relationship(back_populates="recipient")
    campaign_donations: List["CampaignDonation"] = Relationship(back_populates="recipient")
    financial_disclosures: List["FinancialDisclosure"] = Relationship(back_populates="politician")
    social_media_accounts: List["SocialMediaAccount"] = Relationship(back_populates="politician")

class PoliticalPosition(AuditableBase, table=True):
    """Tracks each office held by a politician over their career."""
    __tablename__ = "political_positions"
    
    id: int = Field(default=None, primary_key=True)
    title: str  # e.g., "Senator", "Representative", "Governor"
    jurisdiction: str  # e.g., "United States - California", "New York City"
    chamber: Optional[Chamber] = None
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = Field(default=False)
    
    politician_id: int = Field(foreign_key="politicians.id")
    politician: Politician = Relationship(back_populates="positions")
    
class PartyAffiliation(AuditableBase, table=True):
    """Tracks a politician's party history, as they can change parties."""
    __tablename__ = "party_affiliations"
    
    id: int = Field(default=None, primary_key=True)
    party_name: str  # e.g., "Democratic", "Republican", "Independent"
    start_date: date
    end_date: Optional[date] = None
    
    politician_id: int = Field(foreign_key="politicians.id")
    politician: Politician = Relationship(back_populates="party_affiliations")

class Bill(AuditableBase, table=True):
    """Represents a piece of legislation."""
    __tablename__ = "bills"
    
    id: int = Field(default=None, primary_key=True)
    bill_number: str = Field(index=True) # e.g., "H.R. 3233"
    title: str
    summary: Optional[str] = None
    congress_session: int # e.g., 117 for the 117th Congress
    introduced_date: date
    status: str # e.g., "Introduced", "Passed House", "Became Law"
    
    sponsor_id: Optional[int] = Field(default=None, foreign_key="politicians.id")
    sponsor: Optional[Politician] = Relationship(back_populates="sponsored_bills")
    
    votes: List["Vote"] = Relationship(back_populates="bill")

class Vote(AuditableBase, table=True):
    """Records a specific politician's vote on a specific bill."""
    __tablename__ = "votes"
    
    id: int = Field(default=None, primary_key=True)
    vote_date: datetime
    position: VotePosition
    roll_call_number: int
    chamber: Chamber
    
    politician_id: int = Field(foreign_key="politicians.id")
    politician: Politician = Relationship(back_populates="votes")
    
    bill_id: int = Field(foreign_key="bills.id")
    bill: Bill = Relationship(back_populates="votes")

class Gift(AuditableBase, table=True):
    """A reported gift received by a politician."""
    __tablename__ = "gifts"
    
    id: int = Field(default=None, primary_key=True)
    description: str
    value: float
    report_date: date
    donor: str  # The source of the gift itself
    
    recipient_id: int = Field(foreign_key="politicians.id")
    recipient: Politician = Relationship(back_populates="gifts_received")

class CampaignDonation(AuditableBase, table=True):
    """A single campaign finance donation."""
    __tablename__ = "campaign_donations"

    id: int = Field(default=None, primary_key=True)
    donor_name: str
    donor_type: str  # e.g., "Individual", "PAC", "Corporation"
    amount: float
    date: date
    
    recipient_id: int = Field(foreign_key="politicians.id")
    recipient: Politician = Relationship(back_populates="campaign_donations")

class FinancialDisclosure(AuditableBase, table=True):
    """Links to a personal financial disclosure report (e.g., assets, liabilities)."""
    __tablename__ = "financial_disclosures"

    id: int = Field(default=None, primary_key=True)
    report_year: int
    filing_date: date
    document_url: str
    
    politician_id: int = Field(foreign_key="politicians.id")
    politician: Politician = Relationship(back_populates="financial_disclosures")
    # For more detail, you could add Asset, Liability, and Transaction tables
    # that link back to this disclosure.

class Committee(AuditableBase, table=True):
    """A legislative committee."""
    __tablename__ = "committees"
    
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    chamber: Chamber
    
    members: List["CommitteeMembership"] = Relationship(back_populates="committee")

class CommitteeMembership(AuditableBase, table=True):
    """Association table linking politicians to committees over time."""
    __tablename__ = "committee_memberships"
    
    id: int = Field(default=None, primary_key=True)
    role: str # e.g., "Chair", "Ranking Member", "Member"
    start_date: date
    end_date: Optional[date] = None
    
    politician_id: int = Field(foreign_key="politicians.id")
    politician: Politician = Relationship(back_populates="committee_memberships")
    
    committee_id: int = Field(foreign_key="committees.id")
    committee: Committee = Relationship(back_populates="members")

class SocialMediaAccount(AuditableBase, table=True):
    __tablename__ = "social_media_accounts"
    
    id: int = Field(default=None, primary_key=True)
    platform: str  # "Twitter", "Facebook", "Instagram"
    handle_or_url: str
    
    politician_id: int = Field(foreign_key="politicians.id")
    politician: Politician = Relationship(back_populates="social_media_accounts")
