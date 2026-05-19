# Milestone Mapping: Course Requirements → Project Deliverables

This document maps the **SWE4403 / CS4015** course milestones to your project deliverables. Use this as your primary planning guide.

---

## Overview

| Milestone | Title | Week | Weight | Git Tag | ARC42 Sections |
|-----------|-------|------|--------|---------|----------------|
| **M0** | Team Formation | 2 | Pass/Fail | — | — |
| **M1** | Project Proposal | 4 | 8% | `v1.0-proposal` | §1–2 |
| **M2** | Architecture Definition | 5 | 10% | `v2.0-definition` | §3–4 |
| **M3** | Pattern Implementation | 8 | 12% | `v3.0-implementation` | §5 |
| **M4** | Evolution & Refinement | 10 | 10% | `v4.0-evolution` | §6 |
| **M5** | Tech Stack Retrospective | 12 | 10% | `v5.0-tooling` | §7 |
| **Final** | Delivery & Demo | 13 | 50% | `v6.0-final` | §1–8 (complete) |

---

## Milestone 0: Team Formation

**Due: Week 2** | **Weight: Pass/Fail**

### Deliverables

- [ ] Team of 3–4 students formed
- [ ] Project selection finalized
- [ ] Team contract signed by all members
- [ ] GitHub repository created/forked
- [ ] All team members have repository access
- [ ] README updated with team information

### Team Contract Must Include

1. Team member names and contact information
2. Roles and responsibilities
3. Communication plan (tools, meeting frequency)
4. Conflict resolution process
5. Work distribution agreement
6. Signatures from all members

### Repository Setup

```
your-project-repo/
├── README.md                 # Updated with team info
├── docs/
│   ├── team-contract.pdf     # Signed contract
│   └── meeting-notes/        # For ongoing documentation
└── .gitignore
```

---

## Milestone 1: Project Proposal

**Due: Week 4** | **Weight: 8%** | **Tag: `v1.0-proposal`**

### Deliverables

- [ ] **ARC42 Section 1:** Introduction and Goals
- [ ] **ARC42 Section 2:** Constraints
- [ ] **Context Diagram:** C4 Level 1 showing system boundary
- [ ] **Initial ADRs:** Document early technology decisions
- [ ] Git tag: `v1.0-proposal`

### Required Content

| ARC42 Section | What to Include |
|---------------|-----------------|
| **§1.1 Requirements Overview** | What problem does this system solve? |
| **§1.2 Quality Goals** | Top 3 quality attributes, ranked with rationale |
| **§1.3 Stakeholders** | Who cares about this system? What do they need? |
| **§2.1 Technical Constraints** | Technology limitations |
| **§2.2 Organizational Constraints** | Timeline, team size, skills |
| **§2.3 Conventions** | Coding standards, documentation format |

### Assessment Focus

Clarity of problem definition. Are constraints realistic? Do quality goals have clear priorities?

---

## Milestone 2: Architecture Definition

**Due: Week 5** | **Weight: 10%** | **Tag: `v2.0-definition`**

### Deliverables

- [ ] **ARC42 Section 3:** Scope & Context
- [ ] **ARC42 Section 4:** Solution Strategy
- [ ] **Container Diagram:** C4 Level 2 showing containers (API, DB, UI)
- [ ] **Style Selection:** Justification for chosen architectural style
- [ ] **Updated ADRs:** Document major technology/framework decisions
- [ ] Git tag: `v2.0-definition`

### Required Content

| ARC42 Section | What to Include |
|---------------|-----------------|
| **§3.1 Business Context** | External actors and interfaces |
| **§3.2 Technical Context** | Protocols, APIs, data formats |
| **§4.1 Technology Decisions** | Key technology choices with rationale |
| **§4.2 Top-Level Decomposition** | How system is broken into parts |
| **§4.3 Approach to Quality Goals** | How architecture addresses quality attributes |

### Assessment Focus

Logical connection between Constraints (M1) and Solution (M2). ADRs should show evidence-based reasoning.

---

## Milestone 3: Pattern Implementation

**Due: Week 8** | **Weight: 12%** | **Tag: `v3.0-implementation`**

### Deliverables

- [ ] **Walking Skeleton:** End-to-end connectivity (Frontend → Backend → DB)
- [ ] **Pattern Code:** Implementation of 2+ GoF patterns with inline documentation
- [ ] **ARC42 Section 5:** Building Block View (Component Diagram)
- [ ] **Testing Foundation:** CI pipeline with automated tests
- [ ] **Code Coverage:** Minimum 50% on core business logic
- [ ] **Traceability:** Comments linking code back to ARC42 docs
- [ ] Git tag: `v3.0-implementation`

### What is a Walking Skeleton?

A tiny implementation that connects all major architectural components end-to-end. It proves the architecture works before you build features.

Example: User clicks button → Frontend calls API → Backend queries DB → Response displayed

### Assessment Focus

Correct application of design patterns. Technical feasibility of the skeleton. Test infrastructure readiness.

---

## Milestone 4: Evolution & Refinement

**Due: Week 10** | **Weight: 10%** | **Tag: `v4.0-evolution`**

### Deliverables

- [ ] **Refactoring Log:** Evidence of improving code based on SOLID principles (before/after examples)
- [ ] **Change Scenario Response:** Adaptation to instructor-issued requirement change
- [ ] **ARC42 Section 6:** Runtime View (sequence diagrams for key use cases)
- [ ] **Updated ARC42:** Documentation must match the new code reality
- [ ] Git tag: `v4.0-evolution`

### Change Scenario

> ⚠️ **The instructor will announce a requirement change in Week 8.** You have approximately 2 weeks to adapt your architecture.

This simulates real-world requirement volatility. Your architecture's quality is measured by how gracefully it accommodates change.

### Assessment Focus

Ability to modify architecture without breaking core constraints. Evidence of principled refactoring.

---

## Milestone 5: Tech Stack Retrospective

**Due: Week 12** | **Weight: 10%** | **Tag: `v5.0-tooling`**

### Deliverables

- [ ] **Decision Matrix:** Weighted scoring of tools/frameworks used, with hindsight analysis
- [ ] **ADR Retrospective:** Review of all ADRs—which decisions held up? Which would you change?
- [ ] **ARC42 Section 7:** Deployment View (infrastructure diagram, Docker/K8s config)
- [ ] **License Audit:** List of all 3rd-party dependencies, their licenses, and compliance status
- [ ] **Ethics & Accessibility Statement:** Brief statement on ethical considerations and accessibility features
- [ ] Git tag: `v5.0-tooling`

### Decision Matrix Template

| Tool/Framework | Criteria 1 | Criteria 2 | Criteria 3 | Score | Hindsight |
|----------------|------------|------------|------------|-------|-----------|
| PostgreSQL | 4 | 5 | 3 | 12 | Would choose again |
| Framework X | 3 | 2 | 4 | 9 | Would reconsider |

### Assessment Focus

Evidence-based reflection. Did your initial choices hold up? What would you do differently?

---

## Final Delivery & Demo

**Due: Week 13** | **Weight: 50%** | **Tag: `v6.0-final`**

### Deliverables

- [ ] **Source Code:** Final release tag in GitHub with README and build instructions
- [ ] **Final ARC42:** Complete PDF documentation (Sections 1–8)
- [ ] **Live Demo:** 12-minute team presentation + 8-minute Q&A
- [ ] **Test Report:** Final coverage report (target: 70%+ on core modules)
- [ ] **Peer Evaluation:** Confidential assessment of teammate contributions (D2L survey)
- [ ] Git tag: `v6.0-final`

### Demo Requirements

| Segment | Duration | Content |
|---------|----------|---------|
| **Presentation** | 12 min | System overview, architecture walkthrough, live demo |
| **Q&A** | 8 min | Instructor questions on design decisions |

**All team members must present.** Prepare to explain any architectural decision.

### Final ARC42 Contents

Your complete documentation must include:

| Section | Title | Content |
|---------|-------|---------|
| §1 | Introduction & Goals | Requirements, quality goals, stakeholders |
| §2 | Constraints | Technical, organizational, conventions |
| §3 | Context & Scope | Business and technical context |
| §4 | Solution Strategy | Technology decisions, decomposition approach |
| §5 | Building Block View | Component diagrams (C4 Level 3) |
| §6 | Runtime View | Sequence diagrams for key scenarios |
| §7 | Deployment View | Infrastructure, deployment mapping |
| §8 | Crosscutting Concepts | Domain model, error handling, security, logging |

### Assessment Focus

Holistic evaluation: Does the documentation match the code? Can you defend your decisions?

---

## ARC42 Section Progression

```
M1 (Week 4)     M2 (Week 5)     M3 (Week 8)     M4 (Week 10)    M5 (Week 12)    Final (Week 13)
    │               │               │                │               │               │
    ▼               ▼               ▼                ▼               ▼               ▼
  §1-2    →      §3-4      →      §5       →       §6       →      §7       →    §1-8
 Goals &       Context &      Building         Runtime        Deployment      Complete
Constraints    Strategy       Blocks            View            View
```

---

## Git Tag Summary

| Tag | Milestone | What It Captures |
|-----|-----------|------------------|
| `v1.0-proposal` | M1 | Initial goals, constraints, context diagram |
| `v2.0-definition` | M2 | Architecture definition, container diagram |
| `v3.0-implementation` | M3 | Walking skeleton, patterns, tests |
| `v4.0-evolution` | M4 | Change scenario response, refactoring |
| `v5.0-tooling` | M5 | Retrospective, deployment view |
| `v6.0-final` | Final | Complete system, all documentation |

---

## Tips for Success

### Start Early
- M1 → M2 is only **1 week**. Start M2 work immediately after submitting M1.
- Architecture decisions made early prevent expensive rework later.

### Document As You Go
- Write ADRs when you make decisions, not at the end.
- Keep ARC42 sections updated incrementally.

### Prepare for the Change Scenario
- Build your architecture to be modular.
- If a change breaks everything, your architecture has a problem.

### The Final is 50%
- Don't treat milestones as isolated assignments.
- Everything builds toward the final delivery and demo.

---

## Quick Reference

| Week | Milestone | Key Deliverable | Tag |
|------|-----------|-----------------|-----|
| 2 | M0 | Team contract, repo setup | — |
| 4 | M1 | ARC42 §1–2, C4 Level 1 | `v1.0-proposal` |
| 5 | M2 | ARC42 §3–4, C4 Level 2 | `v2.0-definition` |
| 8 | M3 | Walking skeleton, 2+ patterns, 50% coverage | `v3.0-implementation` |
| 10 | M4 | Change scenario response, ARC42 §6 | `v4.0-evolution` |
| 12 | M5 | Retrospective, deployment, license audit | `v5.0-tooling` |
| 13 | Final | Complete system, demo, 70% coverage | `v6.0-final` |
