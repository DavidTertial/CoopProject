# ADR-004: Use Terminal-Based Alerts for Notifications

**Date:** 2026-02-01  
**Status:** Accepted  
**Deciders:** Pavitra Srivastava, Ibrahim Abdulazizov, Luqmaan Syed, David Ajaero  
**Quality Attribute(s):** Availability, Maintainability, Cost Efficiency  



## Context

The healthcare IoT monitoring system must notify medical staff when sensor data indicates a critical or emergency condition. Alerts are a core system feature and must be reliable and timely.

However, the project has the following constraints:

- **Zero budget** — Paid SMS or email services are not allowed  
- **Academic prototype** — Real-world integration is not mandatory  
- **Short timeline** — Implementation must be simple and testable  
- **Modular monolithic architecture** — Alerts must integrate cleanly as a module  

**Key questions we needed to answer:**
- How should the system notify operators about emergencies?
- What option best balances reliability, cost, and simplicity?



## Decision

We will use **terminal-based alerts** as the primary notification mechanism.

Alerts will be printed clearly and prominently to the system console when abnormal sensor readings are detected. The alerting logic will be implemented as a dedicated module, allowing future replacement or extension (e.g., email or SMS) without impacting other modules.



## Alternatives Considered

### Option 1: Email Notifications

**Description:**  
Send alert emails using SMTP or third-party email APIs.

**Pros:**
- More realistic for real-world systems  
- Operators can receive alerts remotely  

**Cons:**
- Requires email servers or third-party services  
- Potential costs or rate limits  



### Option 2: SMS Notifications

**Description:**  
Send SMS alerts using a paid messaging service.

**Pros:**
- Fast and highly visible alerts  
- Very realistic for emergency notifications  

**Cons:**
- Requires paid third-party services  
- Not compatible with zero-budget constraint  
- Additional security and configuration complexity  



## Consequences

### Positive

- No external dependencies or services required  
- Simple and deterministic behavior  
- Easy to implement, debug, and test  
- Fully compliant with course requirements  
- Keeps focus on core system architecture  

### Negative

- Alerts are not delivered to real users  
- Not suitable for production or clinical use  
- Requires manual observation of system output  



## Risks

- **Risk:** Alert mechanism may appear unrealistic for healthcare systems  
  - **Mitigation:** Clearly document that this is a prototype choice and design the module for future extensibility  


