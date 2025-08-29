from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class Politician(SQLModel, table=True):
    __tablename__ = "politicians"

    """
    Represents a politician with their personal and office details.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="Full name of the politician")
    party: str = Field(..., description="Political party affiliation")
    office: str = Field(..., description="Elected office, e.g., Senator or Representative")
    term_start: date = Field(..., description="Start date of the term")
    term_end: date = Field(..., description="End date of the term")
    vote_records: List["VoteRecord"] = Relationship(back_populates="politician")
    gifts: List["Gift"] = Relationship(back_populates="politician")


class VoteRecord(SQLModel, table=True):
    """
    Represents a voting record of a politician.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    bill_name: str = Field(..., description="Name of the bill being voted on")
    vote_date: date = Field(..., description="Date when the vote occurred")
    vote_position: str = Field(..., description="Position taken by the politician (e.g., For, Against, Abstain)")
    politician_id: int = Field(foreign_key="politicians.id")
    politician: "Politician" = Relationship(back_populates="vote_records")


class Gift(SQLModel, table=True):
    """
    Represents a gift received by a politician.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(..., description="Description of the gift")
    value: float = Field(..., description="Monetary value of the gift")
    date_received: date = Field(..., description="Date when the gift was received")
    donor: str = Field(..., description="Name of the donor")
    politician_id: int = Field(foreign_key="politicians.id")
    politician: "Politician" = Relationship(back_populates="gifts")
