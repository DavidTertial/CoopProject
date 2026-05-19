# ADR Retrospective

> **Milestone:** M5 — Tech Stack Retrospective  
> **Date:** 2026-04-02

---

## Purpose

Review all Architecture Decision Records (ADRs) created during the project. Which decisions held up? Which would you change with hindsight?

---

## ADR Summary

| ADR | Title | Date | Status | Verdict |
|-----|-------|------|--------|---------|
| ADR-001 | Terminal Interface | 2026-01-31 | Accepted | ⚠️ Partially |
| ADR-002 | Use Python as Programming Language | 2026-01-31 | Accepted | ✅ Held up |
| ADR-003 | Use MariaDB for Database | 2026-01-31 | Accepted | ✅ Held up |
| ADR-004 | Use Terminal-Based Alerts | 2026-02-01 | Accepted | ✅ Held up |
| ADR-005 | Architectural Style – Modular Monolith | 2026-02-08 | Accepted | ✅ Held up |
| ADR-006 | Sensor Input – Simulated Random Values | 2026-02-07 | Proposed | ⚠️ Partially |

---

## Detailed Review

### ADR-001: Terminal Interface
**Original Decision:** Use a CLI instead of a web or desktop GUI.
**What Happened:** Worked well overall. However, colored alert severity levels mentioned as a risk mitigation were never implemented.
**Verdict:** ⚠️ Partially
**If we could redo it:** Implement colored terminal output for alert severity from the start.

---

### ADR-002: Use Python as Programming Language
**Original Decision:** Use Python for the entire system.
**What Happened:** Correct choice. The team was productive quickly and all requirements were met.
**Verdict:** ✅ Held up
**If we could redo it:** No changes.

---

### ADR-003: Use MariaDB for Database
**Original Decision:** Use MariaDB for storing patient records and sensor readings.
**What Happened:** Worked reliably. Main friction was each developer setting up their own local instance manually.
**Verdict:** ✅ Held up
**If we could redo it:** Set up a shared Docker database instance from the start.

---

### ADR-004: Use Terminal-Based Alerts
**Original Decision:** Print alerts to the terminal instead of using email or SMS.
**What Happened:** Implemented exactly as decided. Fit the zero-budget constraint and the observer pattern makes it easy to swap out later.
**Verdict:** ✅ Held up
**If we could redo it:** No changes.

---

### ADR-005: Modular Monolith Architecture
**Original Decision:** Single deployable app with clear internal module boundaries.
**What Happened:** Worked well. Module separation kept responsibilities clear and testing straightforward.
**Verdict:** ✅ Held up
**If we could redo it:** No changes.

---

### ADR-006: Simulated Sensor Input
**Original Decision:** Use internally generated random values to simulate sensors.
**What Happened:** Made alert testing easy but the random data lacks realistic noise and the thresholds were never validated against real clinical data.
**Verdict:** ⚠️ Partially
**If we could redo it:** Use pre-recorded real sensor datasets for a more realistic final prototype.

---

## Decisions We Wish We'd Made Earlier

List important decisions that were made too late or never formally documented:

1. **Shared database environment:** A shared MariaDB instance from day one would have prevented setup inconsistencies across developers.
2. **Per-patient alert thresholds:** Fixed thresholds applied to all patients regardless of age or condition was never formally documented as a decision despite having real clinical implications.


---

## Key Takeaways

### What Made Good ADRs
- Clear constraints listed upfront (budget, timeline, team size)
- Honest pros and cons for each alternative

### What Made Poor ADRs
- ADR-006 was never moved from "Proposed" to "Accepted"
- Risk mitigations listed in ADRs were not always followed through

### Advice for Future Teams
1. Write the ADR before implementing, not after
2. If a risk mitigation is listed, track it to completion
3. Update ADR status as the project progresses