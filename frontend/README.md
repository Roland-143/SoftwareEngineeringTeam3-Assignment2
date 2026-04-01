# Frontend Skeleton

This folder is intentionally stack-neutral.

## What exists now
- `Dockerfile` placeholder image for a generic workspace container.
- `index.html` placeholder message (no framework assumptions).

## What frontend team should add after stack decision
- Runtime and dependency files (for example `package.json`, `pnpm-lock.yaml`, etc. if using Node-based tooling).
- Source layout and components.
- API integration using backend base URL conventions agreed by the team.
- Updated `frontend/Dockerfile` for the selected stack.

## Required docs to update in same PR
- `docs/ARCHITECTURE_DECISIONS.md`
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`
