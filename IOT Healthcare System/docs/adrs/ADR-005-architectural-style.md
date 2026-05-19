# ADR-006: Architectural Style – Modular Monolith

**Date:** 2026-02-08
**Status:** Accepted
**Deciders:** Pavitra Srivastava, Ibrahim Abdulazizov, Luqmaan Syed, David Ajaero
**Quality Attribute(s):** Maintainability, Modifiability, Simplicity

---

## Context

The system must be implemented within a short academic timeline while remaining easy to understand, test, and deploy. The project does not currently require independent deployment or scaling of individual components, but it must still be structured in a way that avoids tightly coupled or disorganized code.

Key constraints influencing this decision include:

- **Short timeline** — Architecture must be quick to implement and reason about
- **Academic project** — Operational complexity should be minimized
- **Evolving requirements** — Design should allow future changes without major rewrites
- **Need for clarity** — Responsibilities should be clearly separated within the codebase

**Key questions we needed to answer:**

- Should the system be split into multiple services or remain a single deployable unit?
- How can we keep the architecture simple without sacrificing maintainability?
- How do we allow future evolution without premature complexity?

---

## Decision

We will use a **Modular Monolith Architecture**.

The system will be built as a single deployable application to simplify deployment, testing, and debugging. Internally, the system will be decomposed into logical modules, each responsible for a specific domain or functionality. These modules will communicate through internal interfaces while sharing a single relational database.

---

## Alternatives Considered

### Option 1: Microservices Architecture

**Description:**
Split the system into independently deployable services communicating over the network.

**Pros:**

- Independent scaling and deployment
- Strong isolation between services

**Cons:**

- High operational and architectural complexity
- Increased development and debugging overhead
- Not suitable for a short academic timeline

---

### Option 2: Layered Monolithic Architecture

**Description:**
Implement the system as a traditional layered monolith (e.g., presentation, service, persistence layers).

**Pros:**

- Familiar and easy to understand
- Simple initial setup

**Cons:**

- Layer-based organization can lead to feature logic being scattered across layers
- Changes often require touching multiple layers, reducing modifiability

---

## Consequences

### Positive

- Simple deployment and testing process
- Clear separation of responsibilities through internal modules
- Lower complexity compared to distributed architectures
- Easier debugging and reasoning about system behavior
- Provides a clear path for future refactoring into separate services

### Negative

- Entire system must be redeployed for any change
- Shared database can increase coupling if boundaries are not enforced
- Limited ability to scale individual modules independently

---

## Risks

- **Risk:** The system may become tightly coupled if module boundaries are ignored

- **Mitigation:** Enforce clear interfaces and responsibility boundaries between modules

- **Risk:** Architecture may be perceived as less scalable than microservices

- **Mitigation:** Document that the modular monolith allows future extraction of modules if scalability requirements change

---
