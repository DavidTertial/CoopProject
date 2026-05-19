import mariadb
from threading import Lock
from datetime import datetime, timedelta

# Database connection layer uses singleton pattern. It limits number of connection pools to 1. 
# Attempting to create new layer instance does not create new pool. All connections belong to this pool.

class DatabaseConnectionMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnection(metaclass=DatabaseConnectionMeta):

    def __init__(self):

        try:
            self.pool = mariadb.ConnectionPool(
                host="localhost",
                user="backend",
                password="backendpassword",
                database="iotmonitoring",
                port=3306,
                autocommit=True,
                pool_name="health_monitor",
                pool_size=20,
            )
        except mariadb.Error as e:
            print(e)
            raise mariadb.Error

    def initialize(self):

        create_patient_table_sql_query = """
            CREATE TABLE IF NOT EXISTS patient(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                                                name VARCHAR (255),
                                                age INTEGER ,
                                                email VARCHAR (255) UNIQUE);
            """

        create_patient_readings_table_sql_query = """
            CREATE TABLE IF NOT EXISTS patientReadings(
                                                id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                                                patientID INTEGER NOT NULL,
                                                heartRate INTEGER,
                                                bodyTemp decimal(10,3),
                                                bloodOXlevel decimal(10,3),
                                                currTime TIMESTAMP
                                                );
            """

        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(create_patient_table_sql_query)
            cursor.execute(create_patient_readings_table_sql_query)
        except mariadb.Error as e:
            print("Error occured while initializing of the Database")
            print(e)
            raise mariadb.Error
        finally:
            cursor.close()
            conn.close()

    def createPatient(self, name, age, email):
        query_insert_patient_data = """
            INSERT INTO patient (name, age, email) VALUES (?,?,?);
            """

        conn = self.pool.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query_insert_patient_data, (name, age, email))
        except mariadb.Error as e:
            print("Error occured while creating a patient in the Database")
        finally:
            cursor.close()
            conn.close()

    def insertPatientReading(
        self, patientID, heartRate, bodyTemp, bloodOXlevel, currTime
    ):
        query_insert_patient_data = """
            INSERT INTO patientReadings (patientID, heartRate, bodyTemp, bloodOXlevel, currTime) VALUES (?,?,?,?,?);
            """
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                query_insert_patient_data,
                (patientID, heartRate, bodyTemp, bloodOXlevel, currTime),
            )
        except mariadb.Error as e:
            print("Error occured while insering patient readings into the Database")
            print(e)
            raise mariadb.Error
        finally:
            cursor.close()
            conn.close()

    def getPatientReadings(self, patientID, earlierTime, laterTime):
        query_get_patient_readings = """
            SELECT * FROM patientReadings WHERE patientID = ? AND currTime <= ? AND currTime >= ?;
            """
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                query_get_patient_readings, (patientID, laterTime, earlierTime)
            )
            patient_readings = cursor.fetchall()
            return patient_readings
        except mariadb.Error as e:
            print("Error occured while getting patient readings into the Database")
            print(e)
            raise mariadb.Error
        finally:
            cursor.close()
            conn.close()

    def get_last_10_min_readings(self, patient_id: int):
        later = datetime.now()
        earlier = later - timedelta(minutes=10)
        return self.getPatientReadings(patient_id, earlier, later)

    def getAllPatients(self):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM patient")
            return cursor.fetchall()
        except mariadb.Error as e:
            print(e)
            raise e
        finally:
            cursor.close()
            conn.close()

    def getPatientByName(self, name):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, name, age, email FROM patient WHERE name = ?", (name,)
            )
            return cursor.fetchone()
        except mariadb.Error as e:
            print(e)
            raise e
        finally:
            cursor.close()
            conn.close()
