# Architecture Decision Record Template

This template follows the format popularized by Michael Nygard. Use this structure for all ADRs in your project.

---

## What is an ADR?

An **Architecture Decision Record (ADR)** captures an important architectural decision along with its context and consequences. ADRs help future team members (including future you) understand:

- **Why** a decision was made
- **What** alternatives were considered
- **What** trade-offs were accepted

---

## ADR Naming Convention

Save your ADRs with this naming pattern:

```
docs/ADRs/ADR-NNN-short-title.md
```

Examples:
- `ADR-001-use-postgresql-for-persistence.md`
- `ADR-002-observer-pattern-for-notifications.md`
- `ADR-003-rest-over-message-queue.md`

---

## Template

Copy everything below this line for each new ADR:

---

# ADR-NNN: [Short Title of Decision]

**Date:** YYYY-MM-DD

**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

**Deciders:** [List team members involved in this decision]

**Quality Attribute(s):** [Which quality attribute(s) does this decision address? e.g., Performance, Reliability, Maintainability, Scalability — leave blank if not applicable]

---

## Context

[Describe the situation that requires a decision. What is the problem? What constraints exist? What forces are at play?]

**Key questions we needed to answer:**
- [Question 1]
- [Question 2]
- [Question 3]

---

## Decision

[State the decision clearly and concisely. Use active voice: "We will..." not "It was decided..."]

**We will [do X].**

[Optionally elaborate on key aspects of the decision.]

---

## Alternatives Considered

### Option 1: [Name]

**Description:** [Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### Option 2: [Name]

**Description:** [Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### Option 3: [Name] *(if applicable)*

[Same structure as above]

---

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]
- [Positive consequence 3]

### Negative

- [Negative consequence 1 — this is the trade-off we accept]
- [Negative consequence 2]

### Risks

- [Risk 1 and how we might mitigate it]
- [Risk 2]

---

## Related Decisions

- [ADR-XXX: Related decision title] *(if applicable)*
- [Link to external resource if relevant]

---

## Notes

[Any additional context, links to discussions, or implementation notes]

---

# Example ADR

Below is a completed example for reference:

---

# ADR-001: Use PostgreSQL for Data Persistence

**Date:** 2026-01-15

**Status:** Accepted

**Deciders:** Alice Chen, Bob Smith, Carlos Rodriguez

**Quality Attribute(s):** Reliability (data consistency), Maintainability (team familiarity)

---

## Context

Our travel booking application requires a database to store user accounts, bookings, and transaction records. We need to choose a database technology that supports:

- ACID transactions (payment processing requires consistency)
- Complex queries (search and filtering)
- Scalability for expected growth
- Team familiarity (we have 14 weeks)

**Key questions we needed to answer:**
- Do we need relational integrity or is eventual consistency acceptable?
- What's our expected data volume?
- What database skills does our team have?

---

## Decision

**We will use PostgreSQL as our primary database.**

We will use a single PostgreSQL instance for the prototype, with separate schemas for each service domain (users, bookings, payments) to maintain logical separation while keeping operational simplicity.

---

## Alternatives Considered

### Option 1: PostgreSQL

**Description:** Open-source relational database with strong ACID compliance.

**Pros:**
- Strong ACID guarantees for payment transactions
- Excellent support for complex queries
- Team has prior experience from CS 3035
- Free and well-documented

**Cons:**
- Vertical scaling has limits
- Schema changes require migrations

### Option 2: MongoDB

**Description:** Document-oriented NoSQL database.

**Pros:**
- Flexible schema for rapid prototyping
- Easy horizontal scaling
- Good for hierarchical data (booking details)

**Cons:**
- Weaker consistency guarantees
- No team experience
- Transactions across collections added only in recent versions

### Option 3: Database per Service (Mixed)

**Description:** Each microservice owns its database (PostgreSQL for payments, MongoDB for bookings).

**Pros:**
- True microservices independence
- Optimized storage per use case

**Cons:**
- Operational complexity too high for 14-week project
- Cross-service queries become very difficult
- Team would need to learn multiple technologies

---

## Consequences

### Positive

- Payment transactions have ACID guarantees
- Team can leverage existing PostgreSQL knowledge
- Single database simplifies deployment for prototype
- Strong tooling ecosystem (pgAdmin, migrations)

### Negative

- We sacrifice some microservices purity (shared database)
- Schema changes will require coordination
- Not demonstrating "database per service" pattern fully

### Risks

- **Risk:** Shared database could create coupling between services
  - **Mitigation:** Use separate schemas and enforce API boundaries in code
- **Risk:** Performance bottleneck with single instance
  - **Mitigation:** Acceptable for prototype; document scaling path for production

---

## Related Decisions

- ADR-002: Service Communication Strategy (pending)
- ADR-003: ORM Selection (pending)

---

## Notes

- PostgreSQL 15 will be used (latest stable as of project start)
- Connection pooling with PgBouncer if performance issues arise
- Team agreed during 2026-01-14 meeting (see meeting-notes/2026-01-14.md)

---

# ADR Quality Checklist

Before submitting, verify your ADR:

- [ ] **Title** clearly describes the decision
- [ ] **Context** explains WHY a decision was needed
- [ ] **Decision** is stated clearly and directly
- [ ] **Alternatives** include at least 2 options with pros/cons
- [ ] **Consequences** include BOTH positive and negative outcomes
- [ ] **Trade-offs** are explicitly acknowledged
- [ ] **Quality Attribute(s)** identified if this is an architectural tactic
- [ ] **Status** is set correctly
- [ ] **Date** and **Deciders** are filled in

---

# Common ADR Topics for This Course

Consider writing ADRs for decisions like:

| Category | Example Decisions |
|----------|-------------------|
| **Data** | Database selection, ORM choice, caching strategy |
| **Communication** | REST vs. GraphQL, sync vs. async messaging |
| **Architecture** | Monolith vs. microservices, service boundaries |
| **Patterns** | Which GoF patterns and why |
| **Quality Tactics** | Caching for performance, circuit breaker for reliability, retry policies |
| **Technology** | Framework selection, language choice |
| **Security** | Authentication approach, authorization model |
| **Deployment** | Containerization, hosting platform |
| **Testing** | Testing strategy, mock vs. real dependencies |

---

# Further Reading

- [Michael Nygard's Original ADR Article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)
- [Joel Parker Henderson's ADR Templates](https://github.com/joelparkerhenderson/architecture-decision-record)
