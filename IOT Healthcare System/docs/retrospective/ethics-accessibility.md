# Ethics & Accessibility Statement

> **Milestone:** M5 — Tech Stack Retrospective  
> **Date:** 2026-04-02

---

## Purpose

Reflect on the ethical considerations and accessibility features of your system. This is increasingly important in professional software development and aligns with engineering ethics requirements.

---

## Ethical Considerations

### Data Privacy

**What data does your system collect?**

| Data Type | Purpose | Sensitivity | Retention |
|-----------|---------|-------------|-----------|
| Patient name | Identify patient | Medium | Stored until manually deleted |
| Patient age | Health context | Medium | Stored until manually deleted |
| Patient email | Contact identifier | Medium | Stored until manually deleted |
| Heart rate | Detect cardiac anomalies | High | Stored until manually deleted |
| Body temperature | Detect fever / hypothermia | High | Stored until manually deleted |
| Blood oxygen level | Detect hypoxia | High | Stored until manually deleted |


**Privacy measures implemented:**

- [x] Data minimization - only what the system needs is collected
- [ ] Encryption at rest
- [ ] Encryption in transit (HTTPS)
- [ ] User consent for data collection
- [ ] Data deletion capability
- [x] Access controls — MariaDB only accessible on localhost

**Privacy considerations we would address in production:**

- Encrypt the database at rest
- Add patient data deletion capability
- Replace hardcoded credentials with environment variables
- Comply with PIPEDA (Canada) or HIPAA (US) before handling real patient data

---

### Bias and Fairness

**Could your system produce biased outcomes?**

[Describe any algorithms, recommendations, or decisions that could be biased]

Alert thresholds in `observer.py` are fixed for all patients regardless of age or condition:

| Vital Sign | Threshold Used |
|------------|---------------|
| Heart rate | < 50 or > 150 bpm |
| Blood oxygen | < 95% or > 100% |
| Body temperature | < 35.5°C or > 38.5°C |

These may not be appropriate for all patients (e.g. athletes naturally have lower resting heart rates).

**Mitigation measures:**

- Thresholds are not clinically validated — documented as a known limitation
- A production system would support per-patient configurable thresholds

---

### Security

**Security measures implemented:**

- [x] Input validation (CLI validates age as a digit and checks email format in `app.py`)
- [ ] Authentication (no login — anyone with terminal access can use the system)
- [ ] Authorization (no role separation — all users have full access)
- [x] Protection against SQL injection (MariaDB parameterized queries used throughout `database.py`)
- [ ] Secure password storage (hashing)
- [ ] Audit logging

**Known security limitations:**

- No login — anyone with terminal access can view all patient data
- Database credentials are hardcoded in `db/database.py`
- No audit trail of who accessed or changed records

---

### Environmental Impact

**Considerations for production deployment:**

- Resource usage: **Low** — single Python process, lightweight MariaDB instance
- Sensor polling interval is configurable, reducing CPU and DB load when increased
- No data retention policy — `patientReadings` table grows unboundedly in current form

---

## Accessibility

### Current State

The system is a CLI application — standard web accessibility standards (WCAG) do not directly apply, but equivalent considerations for terminal interfaces are addressed below.

**What accessibility features are implemented?**

- [ ] Semantic HTML — N/A (CLI, not a web app)
- [x] Keyboard navigation — all interaction is keyboard-driven by design
- [ ] Screen reader compatibility — not explicitly tested; depends on the user's terminal emulator and OS screen reader (e.g., NVDA, VoiceOver)
- [ ] Color contrast compliance (WCAG AA) — the system uses plain text output with no colour formatting, which avoids contrast issues entirely
- [ ] Alt text for images — N/A
- [ ] Form labels — menu options are numbered and labelled in plain text
- [x] Error messages accessible — validation errors are printed as plain text to stdout (e.g., "Age must be a valid number.")
- [ ] Responsive design — N/A

### WCAG Compliance

**Target level:** A (adapted for CLI context)

**Current assessment:**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Perceivable | ⚠️ | All output is plain text — readable by screen readers in most terminals, but no testing was done |
| Operable | ✅ | Fully keyboard-driven; no mouse required |
| Understandable | ✅ | Menu options are clearly numbered and labelled; error messages are descriptive |
| Robust | ⚠️ | Works in standard terminals; screen reader compatibility not verified |

### Accessibility Improvements for Future

1. Test with screen readers (NVDA, VoiceOver)
2. Add colour-coded alerts using ANSI escape codes with a `--no-color` flag fallback for users who cannot perceive colour
3. If a web or GUI interface is added in the future, follow WCAG 2.1 AA guidelines from the start

---

## Professional Responsibility

As software engineers, we recognize our responsibility to:

- [x] Build software that respects user privacy
- [x] Consider the impact of our systems on all users
- [x] Design for inclusivity and accessibility
- [x] Be transparent about system limitations
- [x] Continuously improve based on user feedback

---

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ACM Code of Ethics](https://www.acm.org/code-of-ethics)
- [IEEE Code of Ethics](https://www.ieee.org/about/corporate/governance/p7-8.html)
- [Engineers Canada Code of Ethics](https://engineerscanada.ca/publications/public-guideline-on-the-code-of-ethics)
