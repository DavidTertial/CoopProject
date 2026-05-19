# Quality Attribute Scenarios

**Project Name:** IoT-Based Healthcare Monitoring System
**Team Members:** Pavitra Srivastava, Ibrahim Abdulazizov, Luqmaan Syed, David Ajaero
**Date:** Feb. 1st, 2026

---

## QAS-01: Alert Response Under Load

**Quality Attribute:** Performance

| Component | Specification |
|-----------|---------------|
| **Source** | A simulated health care sensor |
| **Stimulus** | Patient readings are abnormal |
| **Environment** | All possible sensors are connected to the system |
| **Artifact** | Signal recognition and processing modules, the display module |
| **Response** | Alert message displayed on the CLI (terminal) interface |
| **Response Measure** | An alert must be generated within 200ms in 99% cases of an abnormal reading on a healthcare system |

**Applicable Tactics (Bass Ch. 5):**
- Asynchronous execution: prioritize reading and processing of real-time data and process other system tasks (e.g. data querying) asynchronously
- Minimize interface overhead: minimize the interface overhead by using the CLI (terminal) interface

**Priority Assessment:**
- [ ] Architectural Driver (High Value, High Risk)
- [x] Contractual Guarantee (High Value, Low Risk)
- [ ] Nice-to-Have (Low Value, Low Risk)
- [ ] Potential Risk (Low Value, High Risk)

**Justification:** 

- Swift displaying of patients' health readings alerts is a core requirement of our sysatem; there are existing practices (such as asynchronous code execution) that can ensure this requirement.  

---

## QAS-02: Database fails during active monitoring
 
**Quality Attribute:** Availability
 
| Component | Specification |
|-----------|---------------|
| **Source** | Database Server(MariaDB)|
| **Stimulus** | The database becomes unreachable while sensor data is being saved|
| **Environment** | The normal operation that occurs during active patient monitoring|
| **Artifact** | Code responsible for saving sensor readings and alerts to the database|
| **Response** | The system temporarily stores the incoming sensor data while still monitoring and saves the data once the database is available again|
| **Response Measure** | The failure is detected within 3-5 seconds; no data is lost; stored data successfully saved within 60 seconds after the database recovers |
 
**Applicable Tactics (Bass Ch. 5):**
- Rollback: Ensures partially failed database writes are safely undone and retried later, preventing corrupted data.
- Heartbeat: Periodically checks database availability to detect failures quickly.
 
**Priority Assessment:**
- [x] Architectural Driver (High Value, High Risk)
- [ ] Contractual Guarantee (High Value, Low Risk)
- [ ] Nice-to-Have (Low Value, Low Risk)
- [ ] Potential Risk (Low Value, High Risk)
 
**Justification:**
The database is a critical component of the system. If it fails during active patient monitoring, data loss or downtime could directly affect patient safety.

---

## QAS-03: Modifying Alert Threshold
 
**Quality Attribute:** Modifiability
 
| Component | Specification |
|-----------|---------------|
| **Source** |Dev team |
| **Stimulus** |Required to change or add alert threshold rules for a vital sign (ex. custom heart rate ranges per patient) |
| **Environment** |During scheduled software updates under normal development conditions|
| **Artifact** |Alert evaluation and threshold configuration modules |
| **Response** |Threshold values can be updated without changing core data processing or alert logic|
| **Response Measure** |Threshold changes implemented by 1 developer in ≤ 2 days, affecting only configuration or a single module |
 
**Applicable Tactics (Bass Ch. 5):**
- Increase Semantic Coherence: Alert threshold logic is kept within a dedicated alert module, reducing the impact of changes on unrelated parts of the system.
 
**Priority Assessment:**
- [ ] Architectural Driver (High Value, High Risk)
- [ ] Contractual Guarantee (High Value, Low Risk)
- [x] Nice-to-Have (Low Value, Low Risk)
- [ ] Potential Risk (Low Value, High Risk)

**Justification:**
 

This is less critical than system availability or real-time alert delivery, making it a lower-risk, lower-priority requirement.

