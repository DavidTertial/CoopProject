# ADR-003: Use Maria DB for database

**Date:** 2026-01-31

**Status:** [Accepted]

**Deciders:** [Ibrahim Abdulazizov, Pavitra Srivastava, Luqmaan Syed, David Ajaero ]

**Quality Attribute(s):** Reliability, Maintainability, Availability, Cost Efficiency

---

## Context

Our IoT healthcare monitoring system requires a relational database to store patient records, sensor metadata, sensor readings, and alert events. The database must provide strong consistency guarantees, structured relationships, and reliable operation while remaining easy to deploy and maintain within a course project environment.

Given our choice of a relational data model, we must select between two closely related technologies: MariaDB and MySQL. Both are widely used, SQL-based databases with similar syntax and tooling, but differ in licensing model, development governance, and long-term openness.

**Key questions we needed to answer:**

- Which database best supports open-source development and long-term accessibility?
- Do we need enterprise-only features or advanced proprietary tooling?
- Which option minimizes cost for a student project?

---

## Decision

We will use MariaDB as the primary relational database for data persistence.

MariaDB will be used to store structured system data, including patients, sensors, sensor readings, and alerts, using normalized tables and foreign-key relationships.

---

## Alternatives Considered

### Option 1: MySQL

**Description:**
Widely used relational database managed by Oracle.

**Pros:**

- Large user base and extensive documentation

- Mature ecosystem and strong industry adoption

**Cons:**

- Some advanced features are locked behind proprietary enterprise editions

- Less transparent open-source development model

---

## Consequences

### Positive

- Fully open-source database aligns with academic and cost constraints

- Strong relational integrity for healthcare-related data

- Easy setup and integration with Python backend

### Negative

- Fewer enterprise-grade tools compared to MySQL Enterprise

- Slight learning curve for team members more familiar with MySQL branding

### Risks

- Risk: Data corruption or loss due to improper backup configuration
  Mitigation: Implement regular automated backups and verify restore procedures
- Risk: Limited team familiarity with MariaDB administration tools
  Mitigation: Provide short internal training and maintain setup documentation

---

## Notes

- Database choice supports the system’s reliability and maintainability goals.

---
