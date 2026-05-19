from backend.sensorData import SensorService


def test_get_sensor_data_returns_expected_keys():
    service = SensorService()
    data = service.getSensorData("John Doe")

    assert "Patient_Name" in data
    assert "timestamp" in data
    assert "heart_rate" in data
    assert "body_temp" in data
    assert "blood_ox_level" in data


def test_get_sensor_data_uses_given_patient_name():
    service = SensorService()
    data = service.getSensorData("John Doe")

    assert data["Patient_Name"] == "John Doe"


def test_set_enable_anomalies_changes_ranges():
    service = SensorService()
    service.setEnableAnomalies(True)

    assert service.hr_min == 40
    assert service.hr_max == 160
    assert service.temp_min == 35
    assert service.temp_max == 39
    assert service.bo_min == 90
    assert service.bo_max == 105

def test_disable_anomalies_restores_normal_ranges():
    service = SensorService()
    service.setEnableAnomalies(True)
    service.setEnableAnomalies(False)
    assert service.hr_min == 60
    assert service.hr_max == 100
    assert service.temp_min == 36
    assert service.temp_max == 37
    assert service.bo_min == 95
    assert service.bo_max == 100

def test_normal_readings_within_range():
    service = SensorService()
    service.setEnableAnomalies(False)
    for _ in range(30):
        data = service.getSensorData("Test")
        assert 60 <= data["heart_rate"] <= 100
        assert 36 <= data["body_temp"] <= 37
        assert 95 <= data["blood_ox_level"] <= 100

def test_timestamp_is_string():
    service = SensorService()
    data = service.getSensorData("Test")
    assert isinstance(data["timestamp"], str)