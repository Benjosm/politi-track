from typing import List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Politician(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "politicians"

    id: int = Field(default=None, primary_key=True)
    name: str
    party: str
    office: str
    term_start: date
    term_end: date

    vote_records: List["server.models.VoteRecord"] = Relationship(
        back_populates="politician",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    gifts: List["server.models.Gift"] = Relationship(
        back_populates="politician",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class VoteRecord(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "vote_records"

    id: int = Field(default=None, primary_key=True)
    bill_name: str
    bill_status: str
    vote_position: str
    session_year: int
    politician_id: int = Field(foreign_key="politicians.id")

    politician: "server.models.Politician" = Relationship(
        back_populates="vote_records",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Gift(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "gifts"

    id: int = Field(default=None, primary_key=True)
    description: str
    value: float
    report_date: date
    source: str
    politician_id: int = Field(foreign_key="politicians.id")

    politician: "server.models.Politician" = Relationship(
        back_populates="gifts",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

# Resolve forward references
Politician.update_forward_refs()
VoteRecord.update_forward_refs()
Gift.update_forward_refs()
