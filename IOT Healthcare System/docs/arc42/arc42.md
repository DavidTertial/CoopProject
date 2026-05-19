# ARC42 Architecture Documentation

> **Project:** IoT-Based Healthcare Monitoring System 
> **Team:** Team 9  
> **Last Updated:** February 8th 2026

---

## Documentation Roadmap

| Section | Title | Due | Milestone |
|---------|-------|-----|-----------|
| §1 | Introduction and Goals | Week 4 | M1 |
| §2 | Constraints | Week 4 | M1 |
| §3 | Context and Scope | Week 5 | M2 |
| §4 | Solution Strategy | Week 5 | M2 |
| §5 | Building Block View | Week 8 | M3 |
| §6 | Runtime View | Week 10 | M4 |
| §7 | Deployment View | Week 12 | M5 |
| §8 | Crosscutting Concepts | Week 13 | Final |

**ADRs are documented separately** in `docs/ADRs/` — see `ADR_TEMPLATE.md`

---

# Section 1: Introduction and Goals

> **Due: M1 (Week 4)**

## 1.1 Requirements Overview

**What is the system?**
An IoT monitoring system for use in healthcare that collects data from multiple sensors, processes data to identify problems and alerts medical staff. This system is meant to serve as an alternative to existing expensive solutions.

**Core Features:**
1. Collect data from multiple sensors.
2. Store and process data.
3. Alert medical staff for emergencies.

## 1.2 Quality Goals

| Priority | Quality Attribute | Motivation |
|----------|-------------------|------------|
| 1 | Availability | Delays or downtime can lead to serious medical complications |
| 2 | Performance | The system needs to be able to handle data from multiple patients simultaneously |
| 3 | Security | A system that works with sensitive health data must be immune to manipulation |

## 1.3 Stakeholders

| Role | Description | Expectations |
|------|-------------|--------------|
| End User | Medical Staff | Need a reliable and performant system that is easy to work with |
| Administrator | Management | Needs a customizable and cheap solution that can scale easily |
| Developer | Engineers | Need a well structured system that is documented and is easy to modify |

---

# Section 2: Constraints

> **Due: M1 (Week 4)**

## 2.1 Technical Constraints

| Constraint | Rationale |
|------------|-----------|
| IoT Compatability | The system must be able to accept data from different (simulated) IoT based sensors |
| Architecture | The system must be developed as a **Modular Monolithic Application**. This immplies, single deployable unit, clear internal module boundaries, modules communicate through well-defined internal interfaces, shared database with logical separation |
| Notifications | System must notify opperators either by console logging or preferible real SMS/email |

## 2.2 Organizational Constraints

| Constraint | Rationale |
|------------|-----------|
| 13-week timeline | Course schedule |
| Team of 3-4 students | Course requirement |
| MIT License | The system must be developed under liberal, open-source MIT License |
| Limited Budget | The system must be developed under 0$ CAD |

## 2.3 Conventions

| Convention | Description |
|------------|-------------|
| Coding style | PEP 8 – Style Guide for Python Code, Available: https://peps.python.org/pep-0008/ |
| Documentation | ARC42, C4 and ADRs to document architectural decisions, meeting-notes and retrospective notes for team dynamics documentation |
| Git workflow | Use GIT Feature branches approach, with a "main", "dev" and feature branches. All PRs to "dev" and "main" branches need at leat 1 approval from another team member |

---

# Section 3: Context and Scope

> **Due: M2 (Week 5)**

## 3.1 Business Context

The system is designed for use in healthcare applications that require constant monitoring of multiple patients to identify anomalies. The system acts as a central hub that processes input from any combination of medical devices. The system is meant to be highly customizable and reliable. It uses a detailed text interface to provide information and alerts to medical staff. 

**Context Diagram:**

![C4 Diagram](https://github.com/UNB-SWE4403/wi26-prj01-team-09/blob/main/docs/diagrams/src/C4_level1_diagram.png)

**External Interfaces**

| Interface    | Description                           | Technology      |
| ------------ | ------------------------------------- | --------------- |
| Sensor Input | Receives sensor data                  | Python SensorService with random data generation |
| Notification | Pushes notifications to email and SMS | Not Decided     |
| CLI Alerts   | Alerts staff via terminal interface   | Terminal Output |

## 3.2 Technical Context

| Component            | Technology  | Purpose                                                             |
| -------------------- | ----------- | ------------------------------------------------------------------- |
| Patient Data Storage | Not Decided | Facilitates storage of patient profiles, readings and alert history |
| CLI                  | Terminal    | Allows staff to interact with the system and recieve updates        |
| Monitoring System    | Python      | Processes sensor data to identify anomalies and generate alerts     |
| Notification Service | Not Decided | Delivers alerts via console, email or SMS                           |

---

# Section 4: Solution Strategy

> **Due: M2 (Week 5)**

## 4.1 Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Programming language | Python |  The team already knows it well, which lowers risk. It has good support for databases, testing, and data processing. Performance is sufficient for a prototype system.|
| Web framework |None (CLI-based application) |The system does not require a web interface. A CLI avoids unnecessary complexity and development time. It fits the project scope and constraints. All required interactions can be handled through the terminal. |
| Database | MariaDB |MariaDB provides a reliable relational database at no cost. It fits structured healthcare data well. It integrates cleanly with Python.|
| Messaging |Terminal-based alerts | Terminal output is simple and reliable. It requires no external services or budget. Alerts are immediately visible to operators. The design allows future replacement if needed.|

## 4.2 Top-Level Decomposition

Describe how the system is decomposed. What architectural style are you using?

**Architectural Style:** Modular Monolith Architecture

**Why this style:**    
  
The system is built as a single deployable application to keep deployment and testing simple.
Internally, it is divided into clear modules so responsibilities do not get mixed.
This fits the short timeline and avoids unnecessary architectural complexity.
It also leaves room to refactor functionality into separate services or update individual modules as requirements evolve. The system is decomposed into logical modules that communicate through internal interfaces while sharing a single relational database.




**Container Diagram:**


![C4-level-2 Diagram](https://github.com/UNB-SWE4403/wi26-prj01-team-09/blob/main/docs/diagrams/src/C4_level2_diagram.png)

## 4.3 Approach to Quality Goals

How does your architecture address the quality goals from §1.2?

| Quality Goal | Architectural Approach |
|--------------|----------------------|
|Availability|Patient data is provided through simulated sensors within the system. No external services are required for data ingestion. This reduces failure points and keeps the system available as long as the application is running. |
|Performance| All modules run in the same process, so communication is fast. There is no network overhead between components. This is sufficient for the scale at which the prototype is being developed.|
|Security|Access to stored data is handled through a dedicated database module. Clear module boundaries reduce accidental misuse of sensitive data. |

---

# Section 5: Building Block View

> **Due: M3 (Week 8)**

## 5.1 Level 1: Overall System

*Already shown in §3 Context Diagram*

## 5.2 Level 3: Container Internals

**Component Diagram — IoT Monitoring System:**

![C4-level-3 Diagram](https://github.com/UNB-SWE4403/wi26-prj01-team-09/blob/main/docs/diagrams/src/C4_level3_diagram.png)

### Component Catalog

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| IoT Monitoring System | Add patients to the system, Read generated patient readings, Show readings of the patients in the system | Python, MariaDB |

## 5.3 Design Patterns Applied

| Pattern | Where Applied | Rationale |
|---------|--------------|-----------|
| Observer | `src/backend/observer.py` (`SensorHub`, `DBReadingObserver`) and `src/backend/sensor_runner.py` | The Observer pattern is used so that when new sensor data is generated, the `SensorHub` can notify all attached observers automatically. This improves flexibility because new observers can be added later without changing the sensor generation logic. It also helps separate responsibilities, since the sensor service produces readings while observers handle actions such as saving readings to the database |
| Singleton | Applied to the DatabaseConnection class | The Singleton pattern is used to ensure that only one shared instance of DatabaseConnection is created per runtime process. This is implemented using a metaclass and a lock, which provides thread-safe instance initialization. It gives the system a single access point to the MariaDB connection pool, avoids unnecessary duplication of pool objects, and helps maintain consistent database access throughout the application.
 |


---

# Section 6: Runtime View

> **Due: M4 (Week 10)**

Show how building blocks interact at runtime for key scenarios.

## 6.1 Scenario: Sensor Data Collection and Storage

*Include sequence diagram*

**Description:**
This scenario describes how the system processes and stores new sensor readings. The SensorService generates simulated health data (heart rate, body temperature, and blood oxygen level). The data is sent to the SensorHub, which acts as the subject in the Observer pattern. The SensorHub notifies all attached observers. The DBReadingObserver receives the reading and inserts it into the database using the DatabaseConnection class. The database then persists the reading for future retrieval.

**Sequence Diagram:**

![Sequence Diagram](https://github.com/UNB-SWE4403/wi26-prj01-team-09/blob/main/docs/diagrams/src/scenario1_sequence.png)

## 6.2 Scenario: Adding a New Patient

**Description:**
This scenario describes how a new patient is added to the system through the CLI interface. The user enters patient details such as name, age, and email. The frontend validates the input and sends the request to the backend Service layer. The Service layer calls the DatabaseConnection to insert the new patient into the database. The database stores the patient record and confirms the operation, after which the system provides feedback to the user.

**Sequence Diagram:**

![Sequence Diagram](https://github.com/UNB-SWE4403/wi26-prj01-team-09/blob/main/docs/diagrams/src/scenario2_sequence.png)

## 6.3 Scenario: [Change Scenario Response]

> Document how your system handled the instructor-issued change scenario.

**Change Requested:**

**How Architecture Accommodated It:**

**What Had to Change:**

---

# Section 7: Deployment View

> **Due: M5 (Week 12)**

Describe the technical infrastructure and how software maps to it.

## 7.1 Infrastructure

*Include deployment diagram showing nodes, containers, and network topology.*

The system runs entirely on a single developer/operator machine as a single
Python process. There is no containerization or cloud deployment — the prototype
is designed to run locally. MariaDB is installed and running on the same host.

**Nodes:**

| Node | Description |
|------|-------------|
| Developer / operator machine | Hosts the Python runtime and a local MariaDB instance |
| GitHub Actions runner | Executes the CI pipeline on push/PR to `main` and `dev` |


**Deployment Diagram:**

![Deployment Diagram](https://github.com/UNB-SWE4403/wi26-prj01-team-09/blob/main/docs/diagrams/src/uml_deployment_diagram.png)

## 7.2 Component-to-Infrastructure Mapping

| Component | Deployed On | Notes |
|-----------|-------------|-------|
| `frontend/app.py` (CLI) | Python process | Entry point; run with `python -m frontend.app` |
| `backend/backendService.py` | Python process | Service layer, called by the CLI |
| `backend/sensor_runner.py` | Python process | Runs as a background daemon thread |
| `backend/observer.py` | Python process | In-process Observer pattern — no separate deployment |
| `backend/sensorData.py` | Python process | Simulates sensor hardware in-process |
| `db/database.py` (`DatabaseConnection`) | Python process | Singleton connection pool, connects to MariaDB |
| MariaDB (`iotmonitoring`) | Same host | Stores `patient` and `patientReadings` tables; port 3306 |
| CI pipeline (`ci.yml`) | GitHub Actions | Runs `pytest`, `pytest-cov`, `flake8` on every push |


## 7.3 Configuration

Describe environment-specific configurations.

| Environment | Configuration | Purpose |
|-------------|--------------|---------|
| Development | MariaDB at `localhost:3306`, credentials hardcoded in `db/database.py`. Run with `python -m frontend.app` | Local development and testing |
| CI | No live DB, mock injection, `requirements.txt` dependencies | Automated testing via GitHub Actions |
| Production (hypothetical) | Credentials via environment variables, MariaDB on a dedicated host, connection pool size tuned to patient load, logging to file instead of stdout | Deploying the system in a real hospital/clinic setting |

---

# Section 8: Crosscutting Concepts

> **Due: Final (Week 13)**

Describe approaches that apply across multiple building blocks.

## 8.1 Domain Model

*Include domain model diagram showing key entities and relationships.*

**Domain Model:**

![Domain Model](https://github.com/UNB-SWE4403/wi26-prj01-team-09/blob/main/docs/diagrams/src/iot_healthcare_domain_model.png)

### Key Entities

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| Patient | A monitored individual registered in the system| id, name, age, email |
| PatientReading | A set of vital sign readings for a patient at a point in time | id, patientID, heartRate, bodyTemp, bloodOXlevel, currTime |
| SensorService | Generates simulated vital sign data within configurable ranges | enableAnomalies, hr_min/max, temp_min/max, bo_min/max |
| SensorHub | Runtime subject in the Observer pattern — holds and notifies all observers | observers (list) |
| DBReadingObserver | Observer that persists each reading to the database | database (DatabaseConnection) |
| AlertObserver | Observer that checks readings against thresholds and enqueues alerts | alertQueue |
| Alert | An alert message generated when a vital sign crosses a threshold | message, vitalSign, patientID |
| DatabaseConnection | Singleton connection pool managing all access to MariaDB | pool (ConnectionPool), pool_size: 20 |

## 8.2 Error Handling

How does the system handle errors consistently?

| Error Type | Handling Strategy |
|------------|------------------|
| DB connection failure | `mariadb.Error` caught in `DatabaseConnection.__init__()`, printed to stdout and re-raised — app cannot start without a DB connection |
| DB query failure | Caught per method in `database.py`, printed to stdout, and re-raised to caller |
| Invalid CLI input (age) | Validated in `app.py` — non-numeric age prints `"Age must be a valid number"` and returns without inserting |
| Invalid CLI input (email) | Validated in `app.py` — missing `@` prints `"Please enter a valid email"` and returns |
| Patient not found | `getPatientByName()` returns `None` — checked in `app.py` and `sensor_runner.py` with a user-facing message; sensor runner skips with `continue` |
| Sensor reading insert failure | `mariadb.Error` caught and re-raised in `insertPatientReading()` |

## 8.3 Logging and Monitoring

| Aspect | Approach |
|--------|----------|
| Log format | Plain text printed to stdout via `print()` — no structured format |
| Log levels | None — no distinction between INFO, WARNING, and ERROR output |
| Monitoring | None — no health checks, metrics, or external monitoring |

## 8.4 Security

| Concern | Approach |
|---------|----------|
| Authentication | None — any user with terminal access has full access to all patient data |
| Authorization | None — no role separation between read-only and administrative actions |
| SQL injection | Parameterized queries (`?` placeholders) used throughout `database.py` — injection is prevented |
| Data encryption | None — data is not encrypted at rest or in transit between the app and MariaDB |
| Audit logging | None — no record of who accessed or modified patient data |

## 8.5 Testing Strategy

| Test Type | Scope | Tools |
|-----------|-------|-------|
| Unit | All backend modules — observer, sensor data, backend service, database layer, sensor runner | pytest, unittest.mock |
| Integration | Database layer against a live MariaDB instance | pytest, pytest-order, live MariaDB |
| End-to-end | Not implemented | — |

---

# ADR Index

Architecture Decision Records are maintained separately. See `docs/ADRs/`.

| ADR | Title | Date | Status |
|-----|-------|------|--------|
| ADR-001 | Terminal Interface | 2026-01-31 | Accepted |
| ADR-002 | Use Python as Programming Language | 2026-01-31 | Accepted |
| ADR-003 | Use MariaDB for Database | 2026-01-31 | Accepted |
| ADR-004 | Use Terminal-Based Alerts for Notifications | 2026-02-01 | Accepted |
| ADR-005 | Architectural Style — Modular Monolith | 2026-02-08 | Accepted |
| ADR-006 | Sensor Input — Simulated Random Values | 2026-02-07 | Accepted |

---

# Glossary

| Term | Definition |
|------|------------|
| IoT | Internet of Things — a network of physical devices that collect and exchange data via sensors |
| CLI | Command Line Interface — a text-based interface where users interact by typing commands in a terminal |
| Modular Monolith | An architectural style where the system is deployed as a single unit but internally divided into distinct modules with clear boundaries |
| Observer Pattern | A design pattern where a subject (SensorHub) notifies a list of observers (DBReadingObserver, AlertObserver) automatically when new data is published |
| Singleton Pattern | A design pattern that ensures only one instance of a class exists at runtime — used here for DatabaseConnection |
| MariaDB | An open-source relational database management system used to store patient records and sensor readings |
| Connection Pool | A cache of database connections maintained so they can be reused — avoids the overhead of opening a new connection for every query |
| ADR | Architecture Decision Record — a document that captures an important architectural decision, its context, alternatives considered, and rationale |
| Vital Signs | Measurable physiological indicators monitored by the system — heart rate (bpm), body temperature (°C), and blood oxygen level (%) |
| Anomaly | A sensor reading that falls outside the defined normal threshold range, triggering an alert |
| SensorHub | The central subject in the Observer pattern that receives sensor readings and notifies all registered observers |
| DBReadingObserver | An observer that receives each sensor reading and persists it to the MariaDB database |
| AlertObserver | An observer that checks each sensor reading against alert thresholds and enqueues alert messages when a value is out of range |
| Daemon Thread | A background thread that automatically terminates when the main program exits — used for the sensor runner in this system |
| Parameterised Query | A SQL query that uses placeholders (`?`) instead of inline values to prevent SQL injection attacks |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-31 | | Initial M1 submission (§1–2) |
| 2.0 | 2026-02-08 | | M2 submission (§3–4) |
| 3.0 | 2026-03-01 | | M3 submission (§5) |
| 4.0 | 2026-03-15 | | M4 submission (§6) |
| 5.0 | 2026-04-02 | | M5 submission (§7) |
| 6.0 | 2026-04-10 | | Final submission (§1–8 complete) |

---

## References

- [ARC42 Template](https://arc42.org/overview)
- [C4 Model](https://c4model.com/)
- [Course ADR Template](../adrs/ADR-000-template.md)
- [Milestone Requirements](../MILESTONE_MAPPING.md)

