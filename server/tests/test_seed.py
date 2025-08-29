"""
Unit tests for data seeding functionality.
Verifies that the database is properly seeded with initial data.
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
import pytest

# Import models for table creation and testing
from server.models import Politician, VoteRecord, Gift
from server.database import engine, SessionLocal


def test_seed_row_counts():
    """
    Test that the database contains the expected number of rows for each table.
    Verifies that the data seeding process has populated the database correctly.
    """
    with Session(engine) as session:
        import os
        print(f"Database URL: {engine.url}")
        db_path = str(engine.url).replace("sqlite:///", "")
        print(f"Database path exists: {os.path.exists(db_path)}")
        if os.path.exists(db_path):
            print(f"File size: {os.path.getsize(db_path)}")
        
        # Count rows in each table
        politician_count = session.exec(select(Politician)).all()
        vote_record_count = session.exec(select(VoteRecord)).all()
        gift_count = session.exec(select(Gift)).all()
        
        politician_count = len(politician_count)
        vote_record_count = len(vote_record_count)
        gift_count = len(gift_count)
        
        # Verify minimum row counts as per requirements
        assert politician_count >= 5, f"At least 5 politicians are required, but only {politician_count} were seeded into the database"
        assert vote_record_count > 0, "No vote records were seeded into the database"
        assert gift_count > 0, "No gifts were seeded into the database"
        
        # Verify minimum ratio of votes and gifts per politician
        if politician_count > 0:
            avg_votes_per_politician = vote_record_count / politician_count
            avg_gifts_per_politician = gift_count / politician_count
            assert avg_votes_per_politician >= 10, f"Expected at least 10 vote records per politician, but found average of {avg_votes_per_politician:.2f}"
            assert avg_gifts_per_politician >= 5, f"Expected at least 5 gifts per politician, but found average of {avg_gifts_per_politician:.2f}"


def test_seeded_data_foreign_key_constraints():
    """
    Test that foreign key constraints are properly maintained in the seeded data.
    Verifies that all foreign key references point to valid primary keys in the referenced tables.
    """
    with Session(engine) as session:
        # Get all vote records and check their politician_id references
        vote_records = session.exec(select(VoteRecord)).all()
        for vote_record in vote_records:
            politician = session.get(Politician, vote_record.politician_id)
            assert politician is not None, f"Vote record with id {vote_record.id} references non-existent politician with id {vote_record.politician_id}"
            
        # Get all gifts and check their politician_id references
        gifts = session.exec(select(Gift)).all()
        for gift in gifts:
            politician = session.get(Politician, gift.politician_id)
            assert politician is not None, f"Gift with id {gift.id} references non-existent politician with id {gift.politician_id}"


def test_seeded_data_relationships():
    """
    Test that relationships between models are properly established in the seeded data.
    Verifies that the ORM relationships correctly load associated objects and that
    each politician has the minimum required number of votes and gifts.
    """
    with Session(engine) as session:
        # Get all politicians to verify per-politician requirements
        politicians = session.exec(select(Politician)).all()
        assert len(politicians) >= 5, f"At least 5 politicians are required, but only {len(politicians)} were found"
        
        # Verify that each politician has the minimum required number of records
        for politician in politicians:
            assert len(politician.vote_records) >= 10, f"Politician {politician.name} should have at least 10 vote records, but has {len(politician.vote_records)}"
            assert len(politician.gifts) >= 5, f"Politician {politician.name} should have at least 5 gifts, but has {len(politician.gifts)}"
        
        # Test bidirectional access for a politician's vote records
        first_politician = politicians[0]
        for vote_record in first_politician.vote_records:
            assert vote_record.politician is not None
            assert vote_record.politician.id == first_politician.id
            assert vote_record.politician.name == first_politician.name
        
        # Test bidirectional access for a politician's gifts
        for gift in first_politician.gifts:
            assert gift.politician is not None
            assert gift.politician.id == first_politician.id
            assert gift.politician.name == first_politician.name


def test_seeded_data_integrity():
    """
    Test that the seeded data maintains data integrity by verifying that
    required fields are not null and data is consistent across related tables.
    """
    with Session(engine) as session:
        # Check that all politicians have required fields
        politicians = session.exec(select(Politician)).all()
        for politician in politicians:
            assert politician.name is not None
            assert politician.party is not None
            assert politician.office is not None
            assert politician.term_start is not None
            assert politician.term_end is not None
        
        # Check that all vote records have required fields
        vote_records = session.exec(select(VoteRecord)).all()
        for vote_record in vote_records:
            assert vote_record.bill_name is not None
            assert vote_record.bill_status is not None
            assert vote_record.vote_position is not None
            assert vote_record.session_year is not None
            assert vote_record.politician_id is not None
        
        # Check that all gifts have required fields
        gifts = session.exec(select(Gift)).all()
        for gift in gifts:
            assert gift.description is not None
            assert gift.value is not None
            assert gift.report_date is not None
            assert gift.source is not None
            assert gift.politician_id is not None
