import queue
from unittest.mock import Mock
from backend.observer import Observer, SensorHub, DBReadingObserver, AlertObserver


def test_sensor_hub_attach_adds_observer():
    hub = SensorHub()
    observer = Mock()

    hub.attach(observer)

    assert observer in hub.observers


def test_db_reading_observer_calls_database_insert():
    fake_db = Mock()
    observer = DBReadingObserver(fake_db)

    fake_reading = {
        "patient_id": 1,
        "heart_rate": 80,
        "body_temp": 36.7,
        "blood_ox_level": 98,
        "timestamp": "2026-03-06 15:00:00",
    }

    observer.update(fake_reading)

    fake_db.insertPatientReading.assert_called_once_with(
        1, 80, 36.7, 98, "2026-03-06 15:00:00"
    )

def test_sensor_hub_detach_removes_observer():
    hub = SensorHub()
    observer = Mock()
    hub.attach(observer)
    hub.detach(observer)
    assert observer not in hub.observers

def test_sensor_hub_publish_calls_all_observers():
    hub = SensorHub()
    obs1, obs2 = Mock(), Mock()
    hub.attach(obs1)
    hub.attach(obs2)
    reading = {"patient_id": 1, "heart_rate": 75, "body_temp": 36.5, "blood_ox_level": 98, "timestamp": "2026-01-01"}
    hub.publish(reading)
    obs1.update.assert_called_once_with(reading)
    obs2.update.assert_called_once_with(reading)

def test_sensor_hub_publish_no_observers():
    hub = SensorHub()
    # should not raise
    hub.publish({"patient_id": 1, "heart_rate": 75, "body_temp": 36.5, "blood_ox_level": 98, "timestamp": "2026-01-01"})

def test_alert_observer_heart_rate_too_low():
    q = queue.Queue()
    observer = AlertObserver(q)
    observer.update({"patient_id": 1, "heart_rate": 40, "body_temp": 36.5, "blood_ox_level": 98})
    assert not q.empty()

def test_alert_observer_heart_rate_too_high():
    q = queue.Queue()
    observer = AlertObserver(q)
    observer.update({"patient_id": 1, "heart_rate": 160, "body_temp": 36.5, "blood_ox_level": 98})
    assert not q.empty()

def test_alert_observer_oxygen_too_low():
    q = queue.Queue()
    observer = AlertObserver(q)
    observer.update({"patient_id": 1, "heart_rate": 75, "body_temp": 36.5, "blood_ox_level": 90})
    assert not q.empty()

def test_alert_observer_temp_too_high():
    q = queue.Queue()
    observer = AlertObserver(q)
    observer.update({"patient_id": 1, "heart_rate": 75, "body_temp": 39.5, "blood_ox_level": 98})
    assert not q.empty()

def test_alert_observer_temp_too_low():
    q = queue.Queue()
    observer = AlertObserver(q)
    observer.update({"patient_id": 1, "heart_rate": 75, "body_temp": 34.0, "blood_ox_level": 98})
    assert not q.empty()

def test_alert_observer_no_alert_normal_reading():
    q = queue.Queue()
    observer = AlertObserver(q)
    observer.update({"patient_id": 1, "heart_rate": 75, "body_temp": 36.5, "blood_ox_level": 98})
    assert q.empty()

def test_base_observer_update_does_nothing():
    obs = Observer()
    obs.update({})  