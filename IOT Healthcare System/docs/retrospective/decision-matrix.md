# Tech Stack Decision Matrix

> **Milestone:** M5 — Tech Stack Retrospective  
> **Date:** 2026-04-02

---

## Purpose

Evaluate the tools and frameworks used in this project with the benefit of hindsight. Would you make the same choices again?

---

## Evaluation Criteria

Define your criteria and weights:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Learning Curve | 9/10 | How quickly could the team become productive? |
| Documentation | 7/10 | Quality and availability of docs/tutorials |
| Performance | 7/10 | Did it meet performance requirements? |
| Team Experience | 8/10 | Prior team familiarity |
| Community Support | 7/10 | Stack Overflow, GitHub issues, forums |
| [Your Criterion] | /10 | [Description] |

---

## Decision Matrix

### Programming Language: Python 3

| Criterion | Score (1-5) | Weight | Weighted Score | Notes |
|-----------|-------------|--------|----------------|-------|
| Learning Curve | 5 | 9/10 | 45/50 | The language features were easy to learn as the project progressed |
| Documentation | 4 | 7/10 | 28/50 | The language is widely used and has good documentation |
| Performance | 4 | 7/10 | 28/50 | The language provided acceptable performance to meet the needs of the project |
| Team Experience | 5 | 8/10 | 40/50 | The team was familiar with the language before the start of the project |
| Community Support | 5 | 7/10 | 35/50 | The language is widely used and was great community support |
| **Total** | 23/25 | | **176/250** |  |

**Verdict:** Would choose again

**Hindsight:** Would choose again

---

### Database: MariaDB

| Criterion | Score (1-5) | Weight | Weighted Score | Notes |
|-----------|-------------|--------|----------------|-------|
| Learning Curve | 4 | 9/10 | 36/50 | MySQL follows standard database management techniques, making it easier to adapt to |
| Documentation | 4 | 7/10 | 28/50 | MySQL is commonly used and has acceptable documentation |
| Performance | 4 | 7/10 | 28/50 | MySQL provided acceptable performance to meet the needs of the project |
| Team Experience | 5 | 8/10 | 40/50 | The team was familiar with MySQL before the start of the project |
| Community Support | 3 | 7/10 | 21/50 | It is possible to find answers to MySQL-related questions on Stackoverflow |
| **Total** | 21/25 | | **153/250** |  |

**Verdict:** Would choose again

**Hindsight:** Set up a Docker database enviroment to host a common instance of the database

---

### Testing Framework: Pytest

| Criterion | Score (1-5) | Weight | Weighted Score | Notes |
|-----------|-------------|--------|----------------|-------|
| Learning Curve | 4 | 9/10 | 36/50 | Pytest was in general easy to adapt to |
| Documentation | 3 | 7/10 | 21/50 | Pytest has acceptable documentation |
| Performance | 4 | 7/10 | 28/50 | Pytest provided acceptable performance to meet the needs of the project |
| Team Experience | 3 | 8/10 | 24/50 | The team was not familiar with Pytest before the start of the project, but had experience with Unit Testing in general |
| Community Support | 4 | 7/10 | 28/50 | It is possible to find answers to Pytest-related questions on Stackoverflow |
| **Total** | 19/25 | | **137/250** |  |

**Verdict:** We'd Reconsider

**Hindsight:** Use a mock database to test database related classes

---

## Summary

### Technologies That Worked Well

1. **[Python 3]:** The language is a versityle programming language, that is easy to learn and build systems quickly.
2. **[MariaDB]:** It is a free to use Database management tool, than comes with great functionality and performance charecteristics

### Technologies We'd Reconsider

1. **[Pytest]:** We did not consder any alternatives, so we are not sure whether there is a better testing framework available for the programming language selected

### Key Lessons Learned

1. Python programming language is a versatile programming language that is easy to learn and build systems quickly
2. MariaDB is a free-to-use database management tool that comes with great functionality and performance characteristics
3. Make sure that the tests for database CRUD classes are independent of the actual database instance and rely on a mock database
