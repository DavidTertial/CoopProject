# ADR-006: Sensor Input

**Date:** 2026-02-07

**Status:** Accepted

**Deciders:** Luqmaan Syed, Ibrahim Abdulazizov, Pavitra Srivastava, David Ajaero

**Quality Attribute(s):** Testability, Modifiability, Performance

---

## Context
The monitoring system needs a way to receive sensor data. It must be able to receive different types of data from multiple sensors simultaneously. It must be performant and easy to test. 

**Key questions we needed to answer:**
- What type of data will the system work with?
- How will the data be formatted?
- How will we test for anomalies?

---

## Decision

We will use randomly generated values to simulate sensor input. This data will be produced internally and fed into the monitoring system to mimic real-time sensor updates.

---

## Alternatives Considered

### Option 1: MQTT

**Description:** Use MQTT to communicate between sensors and monitoring system.

**Pros:**
- Industry standard for IoT
- Built for real world deployment

**Cons:**
- Requires implementation of a complete sensor to system pipeline to be testable.

### Option 2: Pre recorded Sensor Data

**Description:** Periodically read in pre recorded sensor data from a csv. 

**Pros:**
- Data recorded from actual sensors is more realistic.
- Data for different types of sensors is readily available online.

**Cons:**
- Limited data entries makes it difficult to run prolonged tests.
- Difficult to artificially add anomalies to data for testing.
---

## Consequences

### Positive

- Can continuously generate new values, making it easy to run prolonged stress tests.
- Easy to programmatically trigger outliers for testing alert systems.
- No need for external files (CSV) or brokers (MQTT) during the initial development phase.

### Negative

- Interface is not standard and requires changes to ensure compatibility with standard IoT health devices. 
- Randomly generated values may lack the nuanced noise or patterns found in physical hardware.

### Risks

- May not scale well with increased sensor count. Asynchronous implementation can help improve performance. 
