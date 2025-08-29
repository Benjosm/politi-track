import pytest
from sqlmodel import SQLModel, create_engine, inspect, Session
from models import Politician, VoteRecord, Gift
from datetime import date

# Create an in-memory SQLite engine for testing
engine = create_engine("sqlite:///:memory:")

# Set up the database schema before tests run
SQLModel.metadata.create_all(engine)

def test_table_schema():
    """
    Test that each model creates the correct table schema with expected columns,
    data types, nullability, and primary key settings.
    """
    inspector = inspect(engine)
    
    # Test Politician table schema
    assert inspector.has_table("politicians"), "Politicians table does not exist"
    politician_columns = inspector.get_columns("politicians")
    politician_col_names = [col["name"] for col in politician_columns]
    
    expected_politician_cols = ["id", "name", "party", "office", "term_start", "term_end"]
    assert sorted(politician_col_names) == sorted(expected_politician_cols)
    
    # Verify id is primary key and autoincrement
    id_column = next(col for col in politician_columns if col["name"] == "id")
    assert id_column["primary_key"] == 1
    assert "integer" in str(id_column["type"]).lower()
    assert not id_column["nullable"]
    
    # Verify name column
    name_column = next(col for col in politician_columns if col["name"] == "name")
    assert "varchar" in str(name_column["type"]).lower() or "text" in str(name_column["type"]).lower()
    assert not name_column["nullable"]
    
    # Verify party column
    party_column = next(col for col in politician_columns if col["name"] == "party")
    assert "varchar" in str(party_column["type"]).lower() or "text" in str(party_column["type"]).lower()
    assert not party_column["nullable"]
    
    # Verify office column
    office_column = next(col for col in politician_columns if col["name"] == "office")
    assert "varchar" in str(office_column["type"]).lower() or "text" in str(office_column["type"]).lower()
    assert not office_column["nullable"]
    
    # Verify term_start and term_end columns
    term_start_column = next(col for col in politician_columns if col["name"] == "term_start")
    assert "date" in str(term_start_column["type"]).lower()
    assert not term_start_column["nullable"]
    
    term_end_column = next(col for col in politician_columns if col["name"] == "term_end")
    assert "date" in str(term_end_column["type"]).lower()
    assert not term_end_column["nullable"]
    
    # Test VoteRecord table schema
    assert inspector.has_table("vote_records"), "VoteRecords table does not exist"
    vote_record_columns = inspector.get_columns("vote_records")
    vote_record_col_names = [col["name"] for col in vote_record_columns]
    
    expected_vote_record_cols = ["id", "bill_name", "bill_status", "vote_outcome", "session_year", "politician_id"]
    assert sorted(vote_record_col_names) == sorted(expected_vote_record_cols)
    
    # Verify id is primary key
    id_column = next(col for col in vote_record_columns if col["name"] == "id")
    assert id_column["primary_key"] == 1
    assert "integer" in str(id_column["type"]).lower()
    assert not id_column["nullable"]
    
    # Verify bill_name column
    bill_name_column = next(col for col in vote_record_columns if col["name"] == "bill_name")
    assert "varchar" in str(bill_name_column["type"]).lower() or "text" in str(bill_name_column["type"]).lower()
    assert not bill_name_column["nullable"]
    
    # Verify bill_status column
    bill_status_column = next(col for col in vote_record_columns if col["name"] == "bill_status")
    assert "varchar" in str(bill_status_column["type"]).lower() or "text" in str(bill_status_column["type"]).lower()
    assert not bill_status_column["nullable"]
    
    # Verify vote_outcome column
    vote_outcome_column = next(col for col in vote_record_columns if col["name"] == "vote_outcome")
    assert "varchar" in str(vote_outcome_column["type"]).lower() or "text" in str(vote_outcome_column["type"]).lower()
    assert not vote_outcome_column["nullable"]
    
    # Verify session_year column
    session_year_column = next(col for col in vote_record_columns if col["name"] == "session_year")
    assert "integer" in str(session_year_column["type"]).lower()
    assert not session_year_column["nullable"]
    
    # Verify politician_id column (foreign key)
    politician_id_column = next(col for col in vote_record_columns if col["name"] == "politician_id")
    assert "integer" in str(politician_id_column["type"]).lower()
    assert not politician_id_column["nullable"]
    
    # Test Gift table schema
    assert inspector.has_table("gifts"), "Gifts table does not exist"
    gift_columns = inspector.get_columns("gifts")
    gift_col_names = [col["name"] for col in gift_columns]
    
    expected_gift_cols = ["id", "description", "value", "report_date", "source", "politician_id"]
    assert sorted(gift_col_names) == sorted(expected_gift_cols)
    
    # Verify id is primary key
    id_column = next(col for col in gift_columns if col["name"] == "id")
    assert id_column["primary_key"] == 1
    assert "integer" in str(id_column["type"]).lower()
    assert not id_column["nullable"]
    
    # Verify description column
    description_column = next(col for col in gift_columns if col["name"] == "description")
    assert "varchar" in str(description_column["type"]).lower() or "text" in str(description_column["type"]).lower()
    assert not description_column["nullable"]
    
    # Verify value column
    value_column = next(col for col in gift_columns if col["name"] == "value")
    assert "numeric" in str(value_column["type"]).lower() or "float" in str(value_column["type"]).lower()
    assert not value_column["nullable"]
    
    # Verify report_date column
    report_date_column = next(col for col in gift_columns if col["name"] == "report_date")
    assert "date" in str(report_date_column["type"]).lower()
    assert not report_date_column["nullable"]
    
    # Verify source column
    source_column = next(col for col in gift_columns if col["name"] == "source")
    assert "varchar" in str(source_column["type"]).lower() or "text" in str(source_column["type"]).lower()
    assert not source_column["nullable"]
    
    # Verify politician_id column (foreign key)
    politician_id_column = next(col for col in gift_columns if col["name"] == "politician_id")
    assert "integer" in str(politician_id_column["type"]).lower()
    assert not politician_id_column["nullable"]
    
    # Test foreign key constraints
    vote_record_fk = inspector.get_foreign_keys("vote_records")
    assert len(vote_record_fk) == 1
    assert vote_record_fk[0]["referred_table"] == "politicians"
    assert vote_record_fk[0]["referred_columns"] == ["id"]
    assert vote_record_fk[0]["constrained_columns"] == ["politician_id"]
    
    gift_fk = inspector.get_foreign_keys("gifts")
    assert len(gift_fk) == 1
    assert gift_fk[0]["referred_table"] == "politicians"
    assert gift_fk[0]["referred_columns"] == ["id"]
    assert gift_fk[0]["constrained_columns"] == ["politician_id"]

def test_data_lifecycle():
    """
    Test that instances of models can be correctly saved to and loaded from the database.
    This verifies round-trip persistence without data loss or transformation errors.
    """
    # Create test data
    test_politician = Politician(
        name="John Doe",
        party="Democratic",
        office="Senator",
        term_start=date(2020, 1, 1),
        term_end=date(2026, 1, 1)
    )
    
    test_vote_record = VoteRecord(
        bill_name="HB-1001",
        bill_status="Passed",
        vote_outcome="Yes",
        session_year=2023,
        politician_id=1
    )
    
    test_gift = Gift(
        description="Travel expense reimbursement",
        value=1500.00,
        report_date=date(2023, 6, 15),
        source="ABC Corporation",
        politician_id=1
    )
    
    # Use a session to add and commit the instances
    with Session(engine) as session:
        # Add politician first since others depend on it
        session.add(test_politician)
        session.commit()
        
        # Update the foreign key references with the generated politician id
        test_vote_record.politician_id = test_politician.id
        test_gift.politician_id = test_politician.id
        
        # Add the other instances
        session.add(test_vote_record)
        session.add(test_gift)
        session.commit()
        
        # Retrieve instances by primary key
        retrieved_politician = session.get(Politician, test_politician.id)
        retrieved_vote_record = session.get(VoteRecord, test_vote_record.id)
        retrieved_gift = session.get(Gift, test_gift.id)
        
        # Assert that retrieved data matches original data
        assert retrieved_politician is not None
        assert retrieved_politician.name == test_politician.name
        assert retrieved_politician.party == test_politician.party
        assert retrieved_politician.office == test_politician.office
        assert retrieved_politician.term_start == test_politician.term_start
        assert retrieved_politician.term_end == test_politician.term_end
        
        assert retrieved_vote_record is not None
        assert retrieved_vote_record.bill_name == test_vote_record.bill_name
        assert retrieved_vote_record.bill_status == test_vote_record.bill_status
        assert retrieved_vote_record.vote_outcome == test_vote_record.vote_outcome
        assert retrieved_vote_record.session_year == test_vote_record.session_year
        assert retrieved_vote_record.politician_id == test_vote_record.politician_id
        
        assert retrieved_gift is not None
        assert retrieved_gift.description == test_gift.description
        assert retrieved_gift.value == test_gift.value
        assert retrieved_gift.report_date == test_gift.report_date
        assert retrieved_gift.source == test_gift.source
        assert retrieved_gift.politician_id == test_gift.politician_id

def test_relationships():
    """
    Test the integrity of relationships between Politician, VoteRecord, and Gift models.
    Ensures that relationships (e.g., Politician.vote_records, Politician.gifts) correctly load associated objects
    and that bidirectional access works properly.
    """
    with Session(engine) as session:
        # Create a politician
        politician = Politician(
            name="John Doe",
            party="Democratic",
            office="Senator",
            term_start=date(2020, 1, 1),
            term_end=date(2026, 1, 1)
        )
        session.add(politician)
        session.commit()
        
        # Create multiple vote records for this politician
        vote1 = VoteRecord(
            bill_name="HB-1001",
            bill_status="Passed",
            vote_outcome="Yes",
            session_year=2023,
            politician_id=politician.id
        )
        
        vote2 = VoteRecord(
            bill_name="SB-2002",
            bill_status="Failed",
            vote_outcome="No",
            session_year=2023,
            politician_id=politician.id
        )
        
        # Create multiple gifts for this politician
        gift1 = Gift(
            description="Travel expense reimbursement",
            value=1500.00,
            report_date=date(2023, 6, 15),
            source="ABC Corporation",
            politician_id=politician.id
        )
        
        gift2 = Gift(
            description="Conference registration",
            value=800.00,
            report_date=date(2023, 7, 10),
            source="XYZ Inc",
            politician_id=politician.id
        )
        
        # Add all records to the session and commit
        session.add(vote1)
        session.add(vote2)
        session.add(gift1)
        session.add(gift2)
        session.commit()
        
        # Retrieve the politician from the database
        retrieved_politician = session.get(Politician, politician.id)
        
        # Assert that the relationships return the correct number of objects
        assert len(retrieved_politician.vote_records) == 2
        assert len(retrieved_politician.gifts) == 2
        
        # Assert that the vote records are correctly associated
        vote_record_bills = [vr.bill_name for vr in retrieved_politician.vote_records]
        assert "HB-1001" in vote_record_bills
        assert "SB-2002" in vote_record_bills
        
        # Assert that the gifts are correctly associated
        gift_sources = [g.source for g in retrieved_politician.gifts]
        assert "ABC Corporation" in gift_sources
        assert "XYZ Inc" in gift_sources
        
        # Test bidirectional access for vote records
        for vote_record in retrieved_politician.vote_records:
            assert vote_record.politician is not None
            assert vote_record.politician.id == retrieved_politician.id
            assert vote_record.politician.name == retrieved_politician.name
        
        # Test bidirectional access for gifts
        for gift in retrieved_politician.gifts:
            assert gift.politician is not None
            assert gift.politician.id == retrieved_politician.id
            assert gift.politician.name == retrieved_politician.name

def test_constraint_enforcement():
    """
    Test that database constraints prevent insertion of records with missing required fields.
    Asserts that IntegrityError is raised when trying to insert null values into non-nullable columns.
    """
    from sqlalchemy.exc import IntegrityError

    with Session(engine) as session:
        # Test Politician required fields
        with pytest.raises(IntegrityError):
            invalid_politician = Politician(
                name=None,  # required
                party="Democratic",
                office="Senator",
                term_start=date(2020, 1, 1),
                term_end=date(2026, 1, 1)
            )
            session.add(invalid_politician)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_politician = Politician(
                name="John Doe",
                party=None,  # required
                office="Senator",
                term_start=date(2020, 1, 1),
                term_end=date(2026, 1, 1)
            )
            session.add(invalid_politician)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_politician = Politician(
                name="John Doe",
                party="Democratic",
                office=None,  # required
                term_start=date(2020, 1, 1),
                term_end=date(2026, 1, 1)
            )
            session.add(invalid_politician)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_politician = Politician(
                name="John Doe",
                party="Democratic",
                office="Senator",
                term_start=None,  # required
                term_end=date(2026, 1, 1)
            )
            session.add(invalid_politician)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_politician = Politician(
                name="John Doe",
                party="Democratic",
                office="Senator",
                term_start=date(2020, 1, 1),
                term_end=None  # required
            )
            session.add(invalid_politician)
            session.commit()
        session.rollback()

        # Test VoteRecord required fields
        # First, create a valid politician for foreign key
        test_politician = Politician(
            name="Jane Smith",
            party="Republican",
            office="Representative",
            term_start=date(2020, 1, 1),
            term_end=date(2026, 1, 1)
        )
        session.add(test_politician)
        session.commit()

        with pytest.raises(IntegrityError):
            invalid_vote = VoteRecord(
                bill_name=None,  # required
                bill_status="Passed",
                vote_outcome="Yes",
                session_year=2023,
                politician_id=test_politician.id
            )
            session.add(invalid_vote)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_vote = VoteRecord(
                bill_name="HB-1002",
                bill_status=None,  # required
                vote_outcome="Yes",
                session_year=2023,
                politician_id=test_politician.id
            )
            session.add(invalid_vote)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_vote = VoteRecord(
                bill_name="HB-1002",
                bill_status="Passed",
                vote_outcome=None,  # required
                session_year=2023,
                politician_id=test_politician.id
            )
            session.add(invalid_vote)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_vote = VoteRecord(
                bill_name="HB-1002",
                bill_status="Passed",
                vote_outcome="Yes",
                session_year=None,  # required
                politician_id=test_politician.id
            )
            session.add(invalid_vote)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_vote = VoteRecord(
                bill_name="HB-1002",
                bill_status="Passed",
                vote_outcome="Yes",
                session_year=2023,
                politician_id=None  # required
            )
            session.add(invalid_vote)
            session.commit()
        session.rollback()

        # Test Gift required fields
        with pytest.raises(IntegrityError):
            invalid_gift = Gift(
                description=None,  # required
                value=100.0,
                report_date=date(2023, 1, 1),
                source="Company A",
                politician_id=test_politician.id
            )
            session.add(invalid_gift)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_gift = Gift(
                description="Dinner",
                value=None,  # required
                report_date=date(2023, 1, 1),
                source="Company A",
                politician_id=test_politician.id
            )
            session.add(invalid_gift)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_gift = Gift(
                description="Dinner",
                value=100.0,
                report_date=None,  # required
                source="Company A",
                politician_id=test_politician.id
            )
            session.add(invalid_gift)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_gift = Gift(
                description="Dinner",
                value=100.0,
                report_date=date(2023, 1, 1),
                source=None,  # required
                politician_id=test_politician.id
            )
            session.add(invalid_gift)
            session.commit()
        session.rollback()

        with pytest.raises(IntegrityError):
            invalid_gift = Gift(
                description="Dinner",
                value=100.0,
                report_date=date(2023, 1, 1),
                source="Company A",
                politician_id=None  # required
            )
            session.add(invalid_gift)
            session.commit()
        session.rollback()
