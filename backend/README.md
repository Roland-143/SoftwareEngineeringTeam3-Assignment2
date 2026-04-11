# Backend Skeleton

This folder is intentionally stack-neutral.

## What exists now
- `Dockerfile` placeholder image for a generic workspace container.

## What backend team should add after stack decision
- Runtime and dependency files (for example `package.json`, `requirements.txt`, `go.mod`, etc.).
- Source layout (`src/`, `app/`, or equivalent).
- Database connection layer using values from `.env`:
  - `DB_HOST`
  - `DB_PORT`
  - `DB_NAME`
  - `DB_USER`
  - `DB_PASSWORD`
- API contract documentation and endpoint implementations.
- Updated `backend/Dockerfile` for the selected stack.

## Required docs to update in same PR
- `docs/ARCHITECTURE_DECISIONS.md`
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`
