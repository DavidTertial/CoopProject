# ADR-002: Use python as Programming language

**Date:** 2026-01-31

**Status:** [Accepted]

**Deciders:** [Ibrahim Abdulazizov, Pavitra Srivastava, Luqmaan Syed, David Ajaero ]

**Quality Attribute(s):** [Performance, Maintainability, Development Velocity]

---

## Context

Our IoT healthcare monitoring system requires backend services to ingest sensor data, process readings, detect abnormal conditions, and trigger alerts. We need to choose a programming language that supports rapid development, readability, and ease of maintenance within the limited timeline of a course project.

Must provide strong support for:
-Networking
-Concurrency
-Database access
-Testing

Should offer acceptable performance for prototype-scale workloads

**Key questions we needed to answer:**

- Which language allows the fastest and safest development within the project timeline?
- Do we require low-level hardware control or maximum runtime performance?
- What language experience does the team already have?

---

## Decision

We will use Python as the primary programming language for the system.

---

## Alternatives Considered

### Option 1: Java

**Description:**
Statically typed, JVM-based language commonly used in enterprise systems.

**Pros:**
-Strong runtime performance and scalability

-Good support for concurrency and reliability

**Cons:**

- Slower development speed for a short project
- Heavier framework complexity than required
- Harder to write code with

### Option 2: C Programming language

**Description:**
Low-level, compiled programming language.

**Pros:**

- Maximum performance and fine-grained hardware control
- Suitable for embedded and real-time systems

**Cons:**

- too low level and hard to work with databases
- Poor fit for rapid iteration and architectural experimentation

---

## Decision Rationale

Python was chosen based on three quality attribute considerations:

**Maintainability:** Python's readable syntax and enforced style conventions (PEP 8) make the codebase easier to understand and modify. All team members were already familiar with Python, so onboarding cost was zero and code reviews were straightforward. This directly supports our Modifiability QA — modules written in Python are easy to read, test, and change independently.

**Development Velocity:** Python's ecosystem directly covers every requirement — `mariadb` for database access, `pytest` and `unittest.mock` for testing, `threading` and `queue` for concurrency, and GitHub Actions for CI. No additional frameworks were needed. This kept the project on schedule within the 13-week timeline.

---

## Consequences

### Positive

- Faster implementation and iteration
- Easier onboarding and collaboration within the team
- Strong support for testing and debugging

### Negative

- Potential compatibility issues when deploying across different environments or Python versions
- Dependency management can become complex if multiple external libraries are used

### Risks

- Risk: Python may be perceived as unsuitable for production healthcare systems
  Mitigation: Clearly document architectural scalability and optimization paths
- Risk: Memory usage may increase with large datasets
  Mitigation: Optimize data structures and use streaming or chunked processing for large inputs

---

## Notes

-Python aligns with the project’s emphasis on maintainability and architectural clarity.
-Alternative languages can be reconsidered if system requirements change.

---
