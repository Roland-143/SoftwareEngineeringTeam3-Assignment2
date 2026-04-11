# Development Log

Append entries. Do not delete old entries unless they are factually wrong.

## Entry template
- Date:
- Jira:
- Team:
- Author:
- Summary:
- Files changed:
- Verification:
- Blockers:
- Next suggested action:

---

- Date: 2026-04-01
- Jira: PM bootstrap
- Team: DevOps / PM
- Author: Initial repo setup
- Summary: Created repository guide, scope documentation, AI/developer workflow instructions, architecture decision log, handoff template, Jira-to-repo mapping, and generic placeholder Dockerfiles for frontend and backend.
- Files changed: `README.md`, `docs/*`, `frontend/Dockerfile`, `backend/Dockerfile`, `.github/pull_request_template.md`
- Verification: Documentation created and placeholder Dockerfiles prepared for later stack-specific replacement.
- Blockers: Final frontend and backend framework choices are still undecided.
- Next suggested action: Have each team confirm their first Jira issue and update docs as real implementation work begins.

- Date: 2026-04-01
- Jira: PM skeleton hardening
- Team: DevOps / PM
- Author: Codex
- Summary: Converted the repository to a stack-neutral, start-ready skeleton; removed accidental React/Vite assumptions; added PR template; cleaned docs; and aligned compose behavior to database-first startup.
- Files changed: `docker-compose.yml`, `.env.example`, `README.md`, `Makefile`, `scripts/up-scaffold.sh`, `backend/*`, `frontend/*`, `database/init/*`, `.github/pull_request_template.md`, `docs/*`.
- Verification: `docker compose --env-file .env.example config` completes successfully.
- Blockers: Docker daemon access in this environment is unavailable, so full `docker compose up` runtime smoke test was not executed here.
- Next suggested action: Team leads should approve stack choices in Jira and replace placeholder Dockerfiles with real runtime Dockerfiles.

- ---

Date:
April 9, 2026

Jira:
Frontend - Initial View Records Page Implementation

Team:
Frontend Team

Author:
Vansh Mago

Summary:
Set up the frontend development environment and completed the initial implementation of the View Records page using the existing React + Vite template from the GitHub repository. Created a reusable frontend folder structure with separate components, page files, shared types, and mock data. Added the main View Records page with a navbar, summary cards, student records table, empty-state support, and footer. Implemented placeholder student data, sorting by student ID in ascending order, and average score calculation. Replaced the placeholder frontend Dockerfile with a working React + Vite Dockerfile and verified that the frontend builds successfully in Docker. The page was intentionally developed with mock data so that backend integration can later be added with minimal changes.

Files changed:
- `frontend/src/App.tsx`
- `frontend/src/index.css`
- `frontend/src/types/Student.ts`
- `frontend/src/data/mockStudents.ts`
- `frontend/src/pages/ViewRecordsPage.tsx`
- `frontend/src/components/Navbar.tsx`
- `frontend/src/components/SummaryCards.tsx`
- `frontend/src/components/RecordsTable.tsx`
- `frontend/src/components/EmptyState.tsx`
- `frontend/Dockerfile`
- `frontend/.dockerignore`

Verification:
- Upgraded local Node.js version to Node 20 and verified frontend compatibility with Vite.
- Successfully ran the frontend locally using `npm install` and `npm run dev`.
- Confirmed the View Records page renders in the browser with:
  - navbar
  - page heading
  - summary cards
  - student records table
  - footer
- Verified student data is displayed in ascending order by student ID.
- Verified average score calculation displays correctly.
- Verified Docker image builds successfully for the frontend.
- Confirmed Docker runtime port conflict was due to port `5173` already being in use by the local Vite server.

Blockers:
- Backend API is not yet available, so the page currently uses mock placeholder student data.
- Docker run step encountered port conflict when local Vite server and Docker container both attempted to use port `5173`.
- Docker commands currently require `sudo` until Docker permissions are fully configured for the VM user.

Next suggested action:
Coordinate with the backend team to confirm the future student records API response format and endpoint details. Then continue frontend work by either polishing the View Records page further or starting implementation of the Add Records page using the same component-based structure.
