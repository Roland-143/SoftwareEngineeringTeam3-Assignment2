# Team Handoff Notes

Use this file so the next team or next developer can continue work without digging through chat history.

## Handoff template
- From team:
- To team:
- Jira:
- What is complete:
- What is not complete:
- Important files:
- Commands to know:
- Risks / assumptions:
- Recommended next step:

---

- From team: DevOps / PM
- To team: All teams
- Jira: PM bootstrap
- What is complete: Base documentation structure exists. Generic placeholder Dockerfiles exist for frontend and backend. Repo now has a documented workflow for AI and human contributors.
- What is not complete: No final application stack or source code structure has been chosen yet.
- Important files: `README.md`, `docs/PROJECT_SCOPE.md`, `docs/AI_AND_DEV_INSTRUCTIONS.md`, `docs/ARCHITECTURE_DECISIONS.md`.
- Commands to know: Docker commands will depend on the final chosen stack.
- Risks / assumptions: Teams must not start coding without checking the documented scope and decisions first.
- Recommended next step: Database, backend, and frontend teams should each create their initial design notes and append them to the documentation workflow.

- From team: DevOps / PM
- To team: Frontend, Backend, Database, QA
- Jira: PM skeleton hardening
- What is complete: Compose now starts database by default with optional stack-neutral scaffold containers; placeholder frontend/backend guidance files added; docs standardized; PR template restored.
- What is not complete: Final frontend and backend stack decisions plus real implementation files are still pending.
- Important files: `docker-compose.yml`, `.env.example`, `README.md`, `backend/README.md`, `frontend/README.md`, `.github/pull_request_template.md`.
- Commands to know: `make up`, `make up-scaffold`, `make logs`, `make down`, `docker compose --env-file .env.example config`.
- Risks / assumptions: Until stack decisions are documented, any runtime-specific files added by teams may conflict.
- Recommended next step: Finalize stack choices in Jira and record the decision in `docs/ARCHITECTURE_DECISIONS.md` before coding starts.
