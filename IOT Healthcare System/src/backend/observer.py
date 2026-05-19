from datetime import datetime
from typing import Optional, Any
import queue

# from src.db.database import DatabaseConnection
# NOTE:
# The database parameter is typed as `Any` so unit tests and CI can run
# without requiring the MariaDB dependency or a running database server.
# In production, this should be replaced with the real type:
#
#     from src.db.database import DatabaseConnection
#
# and the constructor should be changed to:
#
#     def __init__(self, database: DatabaseConnection) -> None:
#
# This allows DBReadingObserver to work with the real database layer
# while keeping tests lightweight by injecting a mock database object.

class SensorReading:
    patient_id: int
    heart_rate: Optional[int] = None
    body_temp: Optional[float] = None
    blood_ox_level: Optional[float] = None
    timestamp: datetime = datetime.now()


class Observer:
    def update(self, reading: SensorReading) -> None:
        pass


class SensorHub:
    """A hub for managing sensor readings and observers."""

    def __init__(self) -> None:
        self.observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def publish(self, reading: SensorReading) -> None:
        for observer in self.observers:
            observer.update(reading)


class DBReadingObserver:
    """inputs each sensor reading into the database"""

    def __init__(self, database: Any) -> None:
        self.db = database

    def update(self, reading: SensorReading) -> None:
        self.db.insertPatientReading(
            reading["patient_id"],
            reading["heart_rate"],
            reading["body_temp"],
            reading["blood_ox_level"],
            reading["timestamp"]
        )

class AlertObserver:

    def __init__(self, alert_queue: queue.Queue) -> None:
        self.alert_queue = alert_queue

    def update( self, reading: SensorReading) -> None:
        patient_id = reading["patient_id"]
        heart_rate = reading["heart_rate"]
        oxygen = reading["blood_ox_level"]
        temp = reading["body_temp"]

        if ( 50 > heart_rate or heart_rate > 150):
            self.alert_queue.put(f"Heart Rate Alert: {heart_rate} | Patient: {patient_id}")
        if( 95 > oxygen or oxygen > 100):
            self.alert_queue.put(f"Blood Oxygen Alert: {oxygen}% | Patient: {patient_id}")
        if (35.5 > temp or temp > 38.5):
            self.alert_queue.put(f"Temperature Alert: {temp}°C | Patient: {patient_id}")