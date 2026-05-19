from unittest.mock import patch
from backend.backendService import Service


SAMPLE_PATIENT = (1, "J. Smith", 45, "jsmith@gmail.com")
SAMPLE_READINGS = [("r1",), ("r2",)]
SAMPLE_PATIENTS = [
    (1, "J. Smith", 45, "jsmith@gmail.com"),
    (2, "A. Doe", 30, "adoe@gmail.com"),
]


class MockDB:
    def __init__(self):
        self.initialized = False
        self.created_patient = None
        self.last_patient_name = None
        self.last_patient_id = None
        self.last_readings_args = None

    def initialize(self):
        self.initialized = True

    def createPatient(self, name, age, email):
        self.created_patient = (name, age, email)

    def getPatientByName(self, name):
        self.last_patient_name = name
        if name == SAMPLE_PATIENT[1]:
            return SAMPLE_PATIENT
        return None

    def get_last_10_min_readings(self, patient_id):
        self.last_patient_id = patient_id
        return SAMPLE_READINGS

    def getPatientReadings(self, patient_id, earlier, later):
        self.last_readings_args = (patient_id, earlier, later)
        return SAMPLE_READINGS

    def getAllPatients(self):
        return SAMPLE_PATIENTS


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_service_initializes_database(mock_db):
    service = Service()
    assert service.dbConnection.initialized is True


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_add_patient(mock_db):
    service = Service()
    service.add_patient("David", 20, "david@example.com")
    assert service.dbConnection.created_patient == ("David", 20, "david@example.com")


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_get_patient_by_name(mock_db):
    service = Service()
    result = service.get_patient_by_name("J. Smith")
    assert result == SAMPLE_PATIENT
    assert service.dbConnection.last_patient_name == "J. Smith"


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_get_last_10_min_readings(mock_db):
    service = Service()
    result = service.get_last_10_min_readings(1)
    assert result == SAMPLE_READINGS
    assert service.dbConnection.last_patient_id == 1


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_get_all_readings(mock_db):
    service = Service()
    result = service.get_all_readings(1)
    assert result == SAMPLE_READINGS
    assert service.dbConnection.last_readings_args[0] == 1


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_get_patient_last_readings(mock_db):
    service = Service()
    result = service.getPatientLastReadings(1, 15)
    assert result == SAMPLE_READINGS
    assert service.dbConnection.last_readings_args[0] == 1


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_list_patients(mock_db):
    service = Service()
    result = service.list_patients()
    assert result == SAMPLE_PATIENTS


@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_get_patient_by_name_not_found(mock_db):
    service = Service()
    result = service.get_patient_by_name("Nobody")
    assert result is None

@patch("backend.backendService.DatabaseConnection", return_value=MockDB())
def test_list_patients_returns_correct_count(mock_db):
    service = Service()
    result = service.list_patients()
    assert len(result) == 2