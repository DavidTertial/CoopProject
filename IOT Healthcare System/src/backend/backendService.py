from db.database import DatabaseConnection
from datetime import datetime, timedelta

class Service:

    def __init__(self):
        self.dbConnection = DatabaseConnection()
        self.dbConnection.initialize()

    def add_patient(self, name, age, email):
        self.dbConnection.createPatient(name, age, email)

    def get_patient_by_name(self, name):
        return self.dbConnection.getPatientByName(name)

    def get_last_10_min_readings(self, patient_id):
        return self.dbConnection.get_last_10_min_readings(patient_id)
    
    def get_all_readings(self, patient_id):
        return self.dbConnection.getPatientReadings(patient_id, datetime(2000, 1, 1), datetime.now())
    
    def getPatientLastReadings(self, patientID, timeInterval):
        current_time = datetime.now()
        earlier_time = current_time - timedelta(minutes=timeInterval)
        readings = self.dbConnection.getPatientReadings(patientID, earlier_time, current_time)
        return readings
    
    def list_patients(self):
        patients = self.dbConnection.getAllPatients()
        return patients