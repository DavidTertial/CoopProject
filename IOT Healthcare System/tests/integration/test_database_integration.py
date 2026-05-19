from unittest.mock import Mock
from db.database import DatabaseConnection
import mariadb
from datetime import datetime, timedelta
import pytest

dbConn = DatabaseConnection()
test_time = datetime.now()

@pytest.mark.order(1)
def test_initialize():
    
    dbConn.initialize()
    
    conn = dbConn.pool.get_connection()
    cursor = conn.cursor()
    tables = []

    try:
        cursor.execute(
            "show tables;")
        tables = cursor.fetchall()
    except mariadb.Error as e:
        print(e)
        raise e
    finally:
        cursor.close()

    assert ('patient',) in tables
    assert ('patientReadings',) in tables

@pytest.mark.order(2)
def test_create_patient():
    name = "Tomm Pie"
    age = 44
    email = "tpie@unkn.com"
    dbConn.createPatient(name, age, email)
    conn = dbConn.pool.get_connection()
    cursor = conn.cursor()
    dbName = "dadadada"
    dbAge = -1
    dbEmail = "adadawda"
    try:
        cursor.execute(
            "SELECT id, name, age, email FROM patient WHERE name = ? and age = ? and email = ?", (name, age, email))
        dbId, dbName, dbAge, dbEmail = cursor.fetchone()
    except mariadb.Error as e:
        print(e)
        raise e
    finally:
        cursor.close()
    
    assert dbName == name
    assert dbAge == age
    assert dbEmail == email
    assert dbId > 0

@pytest.mark.order(3)
def test_insertPatientReading():
    # This test assumes that a patient with ID == 1 is used for testing purposes and it existis in the database
    patientID = 1
    heartRate = 100
    bodyTemp = 36.6
    bloodOXlevel = 99.9 
    currTime = test_time
    dbConn.insertPatientReading(patientID, heartRate, bodyTemp, bloodOXlevel, currTime)

    conn = dbConn.pool.get_connection()
    cursor = conn.cursor()

    query_get_patient_readings = '''
            SELECT * FROM patientReadings WHERE patientID = ? AND currTime <= ? AND currTime >= ?;
            '''
    
    dbAge, dbId, dbHr, dbTemp, dbOx, dbTime = 0, 0, 0, 0, 0, 0
    try:
        cursor.execute(query_get_patient_readings,
            (patientID, currTime + timedelta(minutes=10), currTime - timedelta(minutes=10)))
        dbAge, dbId, dbHr, dbTemp, dbOx, dbTime = cursor.fetchone()
    except mariadb.Error as e:
        print("Error occured while getting patient readings into the Database")
        print(e)
        raise mariadb.Error
    finally:
        cursor.close()

    assert dbAge > 0
    assert dbId == patientID
    assert dbHr == heartRate
    assert float(dbTemp) == bodyTemp
    assert float(dbOx) == bloodOXlevel

@pytest.mark.order(7)
def test_getPatientByName():
    # This test assumes that a patient with name == Tomm Pie" is existis in the database
    name = "Tomm Pie"
    dbId, dbName, dbAge, dbEmail = dbConn.getPatientByName(name)
    assert dbName == name

@pytest.mark.order(4)
def test_getPatientReadings():
    # This test assumes that a patient with ID == 1 is used for testing purposes and it existis in the database
    patientID = 1
    earlierTime = test_time - timedelta(minutes=2)
    laterTime = test_time + timedelta(minutes=2)
    readings = dbConn.getPatientReadings(patientID, earlierTime, laterTime)
    assert len(readings) > 0

@pytest.mark.order(5)
def test_get_last_10_min_readings():
    # This test assumes that a patient with ID == 1 is used for testing purposes and it existis in the database
    patientID = 1
    ten_min_readings = dbConn.get_last_10_min_readings(patientID)
    assert len(ten_min_readings) > 0

@pytest.mark.order(6)
def test_getAllPatients():
    # This test assumes that a patient with ID == 1 is used for testing purposes and it existis in the database
    patients = dbConn.getAllPatients()
    assert len(patients) > 0.