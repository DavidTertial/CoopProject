# [Project Name]

> **Course:** SWE4403/CS4015 — Software Architecture & Design Patterns  
> **Term:** Winter 2026  
> **Architectural Pattern:** Modular Monolith

---

## Team

| Name | GitHub | Role |
|------|--------|------|
|Pavitra Srivastava |@PavitrSri | Project Lead |
|Ibrakhim Abdulazizov | @IbrakhimUNB |Tech Lead |
|Syed Luqmaan | @sydluqmaan |QA Lead |
| David Ajaero| @DavidTertial |Documentation Lead|

---

## Project Overview

This project involves building an IoT-based healthcare monitoring system that collects vital sign data from simulated sensors. The system processes this data to detect abnormal readings and alerts medical staff when needed. The goal is to create a simple, customizable, and low-cost alternative to existing healthcare monitoring solutions.

---

## Quick Start

### Prerequisites

- Python 3.11+
- MariaDB 10.6+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/UNB-SWE4403/wi26-prj01-team-09.git
cd wi26-prj01-team-09

# Install dependencies
pip install -r requirements.txt

# Run the application
1. Navigate to the src folder
2. run python -m frontend.app

Readings are generated automatically generated, and alerts are displayed whenever an abnormal reading is detected.


```

### Running Tests

```bash
pytest tests/unit/ --cov=src
```

---

## Architecture

**Architectural Pattern:** Modular Monolith

**Key Design Patterns:** Observer, Singleton

📄 [Full Architecture Documentation](docs/arc42/arc42.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [ARC42](docs/arc42/arc42.md) | Full architecture documentation (Sections 1–8) |
| [ADRs](docs/adrs/) | Architecture Decision Records (ADR-001 to ADR-006) |
| [Diagrams](docs/diagrams/) | C4 Level 1–3 diagrams, sequence diagrams, deployment diagram |
| [Retrospective](docs/retrospective/) | M5 deliverables — decision matrix, ethics statement, ADR retrospective |

---

## Project Status

| Milestone | Due | Status | Tag |
|-----------|-----|--------|-----|
| M0: Team Formation | Week 2 | ✅ Complete | — |
| M1: Proposal | Week 4 | ✅ Complete | `v1.0-proposal` |
| M2: Definition | Week 5 | ✅ Complete | `v2.0-definition` |
| M3: Implementation | Week 8 | ✅ | `v3.0-implementation` |
| M4: Evolution | Week 10 | ✅ | `v4.0-evolution` |
| M5: Retrospective | Week 12 | ✅ | `v5.0-tooling` |
| Final Delivery | Week 13 | ✅ | `v6.0-final` |

---

## Repository Structure

```
├── docs/
│   ├── arc42/           # ARC42 architecture documentation
│   ├── adrs/            # Architecture Decision Records
│   ├── diagrams/        # C4 and sequence diagrams
│   ├── meeting-notes/   # Team meeting notes
│   └── retrospective/   # M5 deliverables
├── src/
│   ├── frontend/        # CLI interface (app.py)
│   ├── backend/         # Business logic, observers, sensor runner
│   └── db/              # Database connection layer
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests 
├── .github/workflows/   # CI pipeline (GitHub Actions)
├── requirements.txt     # Python dependencies
├── conftest.py          # Pytest configuration
└── setup.cfg            # Coverage configuration
```

---

## License

[MIT](LICENSE)

---

## Acknowledgments

This project is part of SWE4403/CS4015 at the University of New Brunswick.
