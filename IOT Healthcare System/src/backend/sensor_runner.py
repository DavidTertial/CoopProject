import time

from db.database import DatabaseConnection
from backend.sensorData import SensorService
from backend.observer import SensorHub, DBReadingObserver, AlertObserver


def ensure_patient_exists(db, patient_name):
    patient = db.getPatientByName(patient_name)

    if patient is None:
        print(f"Patient '{patient_name}' not found.")
        return None
    return patient[0]


def run_sensor_stream(patient_names, alert_queue, interval_seconds=4, anomalies=True):
    db = DatabaseConnection()
    db.initialize()

    sensor_service = SensorService()
    sensor_service.setEnableAnomalies(anomalies)

    hub = SensorHub()
    hub.attach(DBReadingObserver(db))
    hub.attach(AlertObserver(alert_queue))

    while True:
        for name in patient_names:
            patient_id = ensure_patient_exists(db, name)
            if patient_id == None:
                continue
            data = sensor_service.getSensorData(name)

            # Add patient ID so observer can store correctly
            data["patient_id"] = patient_id

            # Publish reading to observers
            hub.publish(data)

            # print("Inserted:", data)
            time.sleep(interval_seconds)


if __name__ == "__main__":
    import queue
    alert_queue = queue.Queue()
    run_sensor_stream(["John Doe"], alert_queue, interval_seconds=2, anomalies=False)