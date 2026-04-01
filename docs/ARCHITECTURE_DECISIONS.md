# Architecture Decisions

Use this file to record project-level technical decisions and assumptions.

## Entry template
- Date:
- Jira:
- Team:
- Decision:
- Reason:
- Alternatives considered:
- Impact on other teams:

---

- Date: 2026-04-01
- Jira: PM bootstrap
- Team: DevOps / PM
- Decision: Placeholder Dockerfiles exist for frontend and backend until the final stack is chosen.
- Reason: The team needed a stable repo structure without forcing an early framework choice.
- Alternatives considered: Locking into a specific frontend/backend stack immediately.
- Impact on other teams: Frontend and backend teams must document final stack choice before replacing placeholders.

- Date: 2026-04-01
- Jira: PM skeleton hardening
- Team: DevOps / PM
- Decision: Docker Compose defaults to database-only startup; frontend/backend run as optional scaffold profile containers.
- Reason: Keeps the repository runnable while avoiding hidden stack assumptions before team decisions are finalized.
- Alternatives considered: Running broken placeholder services by default; preselecting Node/React/Express.
- Impact on other teams: Frontend/backend teams can start from clean placeholders and must replace Dockerfiles plus add runtime files after stack decision.
