from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import pytest

def make_mock_db():
    # clear singleton between tests
    from db.database import DatabaseConnection
    DatabaseConnection._instances.clear()
    mock_pool = MagicMock()
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_pool.get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    with patch("db.database.mariadb.ConnectionPool", return_value=mock_pool):
        db = DatabaseConnection()
    return db, mock_cursor

def test_initialize_executes_two_queries():
    db, cursor = make_mock_db()
    db.initialize()
    assert cursor.execute.call_count == 2

def test_create_patient_executes_query():
    db, cursor = make_mock_db()
    db.createPatient("Alice", 30, "alice@example.com")
    cursor.execute.assert_called_once()

def test_insert_patient_reading_executes_query():
    db, cursor = make_mock_db()
    db.insertPatientReading(1, 75, 36.5, 98.0, datetime.now())
    cursor.execute.assert_called_once()

def test_get_all_patients_returns_results():
    db, cursor = make_mock_db()
    cursor.fetchall.return_value = [(1, "Alice", 30, "alice@example.com")]
    result = db.getAllPatients()
    assert result == [(1, "Alice", 30, "alice@example.com")]

def test_get_patient_by_name_found():
    db, cursor = make_mock_db()
    cursor.fetchone.return_value = (1, "Alice", 30, "alice@example.com")
    result = db.getPatientByName("Alice")
    assert result[1] == "Alice"

def test_get_patient_by_name_not_found():
    db, cursor = make_mock_db()
    cursor.fetchone.return_value = None
    result = db.getPatientByName("Nobody")
    assert result is None

def test_singleton_returns_same_instance():
    from db.database import DatabaseConnection
    DatabaseConnection._instances.clear()
    with patch("db.database.mariadb.ConnectionPool", return_value=MagicMock()):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
    assert db1 is db2


def test_get_patient_readings():
    db, cursor = make_mock_db()
    cursor.fetchall.return_value = [(1, 1, 75, 36.5, 98.0, datetime.now())]
    result = db.getPatientReadings(1, datetime.now() - timedelta(minutes=5), datetime.now())
    assert len(result) == 1

def test_get_last_10_min_readings():
    db, cursor = make_mock_db()
    cursor.fetchall.return_value = [(1, 1, 75, 36.5, 98.0, datetime.now())]
    result = db.get_last_10_min_readings(1)
    assert len(result) == 1

def test_get_all_patients_empty():
    db, cursor = make_mock_db()
    cursor.fetchall.return_value = []
    result = db.getAllPatients()
    assert result == []

def test_initialize_calls_execute_twice():
    db, cursor = make_mock_db()
    db.initialize()
    assert cursor.execute.call_count == 2


def test_insert_patient_reading_raises_on_db_error():
    db, cursor = make_mock_db()
    cursor.execute.side_effect = Exception("insert error")
    with pytest.raises(Exception):
        db.insertPatientReading(1, 75, 36.5, 98.0, datetime.now())

def test_get_patient_readings_raises_on_db_error():
    db, cursor = make_mock_db()
    cursor.execute.side_effect = Exception("read error")
    with pytest.raises(Exception):
        db.getPatientReadings(1, datetime.now(), datetime.now())

def test_get_all_patients_raises_on_db_error():
    db, cursor = make_mock_db()
    cursor.execute.side_effect = Exception("fetch error")
    with pytest.raises(Exception):
        db.getAllPatients()

def test_get_patient_by_name_raises_on_db_error():
    db, cursor = make_mock_db()
    cursor.execute.side_effect = Exception("name error")
    with pytest.raises(Exception):
        db.getPatientByName("Alice")

def test_initialize_raises_on_db_error():
    db, cursor = make_mock_db()
    cursor.execute.side_effect = Exception("init error")
    with pytest.raises(Exception):
        db.initialize()