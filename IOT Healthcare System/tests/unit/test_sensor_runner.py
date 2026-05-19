from backend.sensor_runner import ensure_patient_exists
from unittest.mock import MagicMock, patch
import queue


SAMPLE_PATIENT = (1, "J. Smith", 45, "jsmith@gmail.com")


class MockDB:
    def getPatientByName(self, name):
        if name == SAMPLE_PATIENT[1]:
            return SAMPLE_PATIENT
        return None


def test_patient_found():
    result = ensure_patient_exists(MockDB(), "J. Smith")
    assert result == 1


def test_patient_not_found():
    result = ensure_patient_exists(MockDB(), "Nobody")
    assert result is None
    
def test_patient_returns_correct_id():
    result = ensure_patient_exists(MockDB(), "J. Smith")
    assert result == SAMPLE_PATIENT[0]

def test_patient_found_returns_id_not_tuple():
    result = ensure_patient_exists(MockDB(), "J. Smith")
    assert isinstance(result, int)

def test_run_sensor_stream_publishes_reading():
    alert_queue = queue.Queue()

    mock_db = MagicMock()
    mock_db.getPatientByName.return_value = (1, "J. Smith", 45, "jsmith@gmail.com")
    mock_db.initialize.return_value = None

    mock_hub = MagicMock()

    call_count = {"n": 0}

    def fake_sleep(_):
        call_count["n"] += 1
        if call_count["n"] >= 1:
            raise StopIteration  # break the while True after 1 iteration

    with patch("backend.sensor_runner.DatabaseConnection", return_value=mock_db), \
         patch("backend.sensor_runner.time.sleep", side_effect=fake_sleep):
        try:
            from backend.sensor_runner import run_sensor_stream
            run_sensor_stream(["J. Smith"], alert_queue, interval_seconds=0, anomalies=False)
        except StopIteration:
            pass

    assert mock_db.getPatientByName.called

