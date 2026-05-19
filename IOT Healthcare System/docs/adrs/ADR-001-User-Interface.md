# ADR-001: Terminal Interface

**Date:** 2026-01-31

**Status:** Accepted

**Deciders:** Chidubem David Ajaero, Ibrakhim Abdulazizov, Luqmaan Syed, Pavitra Srivastava

**Quality Attribute(s):** Performance, Modifiability, Usability

---

## Context

We need an interface for medical staff to interact with the system. It must display patient readings, show active alerts, and allow adding new patients. The interface must be responsive enough for a healthcare environment and simple enough to build and extend within a 13-week timeline with zero budget.

**Key questions we needed to answer:**
- What interface can we realistically build within the project constraints?
- Does the interface need to support real-time data visualization?
- How does the interface choice affect system performance and modifiability?

---

## Decision

We will use a command line interface (CLI). The terminal displays monitored patients, their readings, and active alerts via a numbered menu. All required interactions — adding patients, viewing readings, receiving alerts — fit naturally into a text-based menu model.

---

## Alternatives Considered

### Option 1: Web GUI (React + Flask)

**Description:** Browser-based interface using a frontend framework and a
REST API backend.

**Pros:**
- Intuitive for non-technical users
- Better data visualization (charts, graphs, dashboards)
- Accessible from any device on the network

**Cons:**
- Requires building and maintaining a separate frontend and backend layer
- Approximately 3× longer development time for the same functionality
- Introduces HTTP overhead between UI and business logic — increases latency
- Framework complexity exceeds what the project scope requires

### Option 2: pyimgui (Desktop GUI)

**Description:** Immediate-mode desktop GUI library for Python.

**Pros:**
- Native desktop performance
- Better data visualization than a CLI

**Cons:**
- Adds an external GUI dependency
- Still requires significant development time for each UI feature
- Team had no prior experience with the library — increases risk

---

## Decision Rationale

The CLI was chosen based on three quality attribute considerations:

**Performance:** All modules run in the same process. The CLI calls backend functions directly with no HTTP layer — function calls complete in microseconds versus 20–100ms for a web request. This matters in a healthcare environment where alert response time is critical (QAS-01 requires alerts within 200ms).

**Modifiability:** A text-based menu is trivially extensible. Adding a new menu option requires one new function and one new branch — no UI framework, no component tree, no CSS. This directly supports our goal of keeping each module independently modifiable (QAS-03).

**Constraints:** Both GUI alternatives violate the zero-budget and 13-week timeline constraints. A web GUI would require a frontend framework, a REST API layer, and significantly more development time. The CLI allows the team to focus on core architectural work rather than UI development.

---

## Consequences

### Positive

- No framework overhead — fast to build, fast to run
- Information-dense output suitable for experienced operators
- Fully keyboard-driven — no mouse required
- Easy to extend without touching other modules
- Resource-light — uses under 10MB of memory versus 50–200MB for a web GUI

### Negative

- Initial learning curve for unfamiliar users
- No data visualization — readings are plain text only
- Staff must be physically present at the terminal to see alerts
- Not suitable as a long-term production interface for a real hospital

### Risks

- **Risk:** Interface is difficult to learn for new staff.
  - **Mitigation:** Numbered menu keeps all options visible on screen at all times.

- **Risk:** Alert volume causes visual overload.
  - **Mitigation:** Alerts are printed before the menu on each refresh. Future
    versions should use colored text to indicate severity levels.

- **Risk:** CLI is perceived as unsuitable for a healthcare product.
  - **Mitigation:** Document explicitly that this is a prototype interface and
    that the modular design allows replacement with a web or desktop GUI without
    changing the backend or sensor logic.