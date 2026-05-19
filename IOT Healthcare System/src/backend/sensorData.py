import random
from datetime import datetime


class SensorService():

    def __init__(self):
        self.enable_anomalies = False
        self.hr_min = 60
        self.hr_max = 100
        self.temp_min = 36
        self.temp_max = 37
        self.bo_min = 95
        self.bo_max = 100

    def setEnableAnomalies(self, enable):
        self.enable_anomalies = enable
        if (enable):
            self.hr_min = 40
            self.hr_max = 160
            self.temp_min = 35
            self.temp_max = 39
            self.bo_min = 90
            self.bo_max = 105

        else:
            self.hr_min = 60
            self.hr_max = 100
            self.temp_min = 36
            self.temp_max = 37
            self.bo_min = 95
            self.bo_max = 100

    def getSensorData(self, patient_name):
        current_time = datetime.now()
        data = {
            "Patient_Name": patient_name,
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "heart_rate": random.randint(self.hr_min, self.hr_max),
            "body_temp": round(random.uniform(self.temp_min, self.temp_max), 1),
            "blood_ox_level": random.randint(self.bo_min, self.bo_max)
        }
        return data
