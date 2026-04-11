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

- Date: 2026-04-10
- Jira: Backend API hardening
- Team: Backend
- Author: Codex
- Summary: Switched the active backend database path to `01_schema.sql` / `02_data.sql`, aligned the runtime DB name to `student_db`, adapted backend queries/inserts to the `Students` + `Enrollments` schema, kept the final rule set at unique student IDs 1 through 10 with 5 seeded demo rows, hardened POST JSON parsing and DB error responses, and added backend-only unittest coverage.
- Files changed: `docker-compose.yml`, `database/docker-compose.yml`, `.env.example`, `database/init/01_schema.sql`, `database/init/02_data.sql`, `backend/app/config.py`, `backend/app/services/student_service.py`, `backend/app/validators.py`, `backend/app/controllers/student_controller.py`, `backend/tests/test_api.py`, `backend/tests/test_student_service.py`, `backend/README.md`, `docs/TEAM_HANDOFF.md`, `docs/DEV_LOG.md`
- Verification: Added unit tests for health, student list shape, average shape, POST validation branches, duplicate-ID conflict mapping, non-duplicate DB constraint mapping, service-level SQL sorting behavior, and two-step insert behavior for the `Students`/`Enrollments` schema. Local test execution still depends on backend Python dependencies being available in the environment.
- Blockers: Docker daemon access is unavailable in this environment, and the local Python environment may not have Flask/mysql-connector installed for direct test execution.
- Next suggested action: Run `python -m unittest discover -s tests` from `backend/` in a backend-ready environment, then reset the database and do a quick Docker smoke test for GET endpoints plus POST inserts using IDs 6 through 10.

- Date: 2026-04-10
- Jira: Backend normalized read semantics
- Team: Backend
- Author: Codex
- Summary: Finished the remaining normalized-schema work by documenting and testing enrollment-list behavior for `GET /api/students`, course-average behavior for `GET /api/students/average`, the unexpected POST failure `500` path, the active `student_db` runtime path, and the final root/backend setup guidance.
- Files changed: `backend/app/services/student_service.py`, `backend/tests/test_api.py`, `backend/tests/test_student_service.py`, `backend/README.md`, `README.md`, `docs/ARCHITECTURE_DECISIONS.md`, `docs/DEV_LOG.md`, `docs/TEAM_HANDOFF.md`, `.env.example`
- Verification: Added service tests that assert SQL joins `Students`, `Enrollments`, and `Courses`, preserves multi-enrollment row order from SQL, and groups averages by course. Added API tests for the new average response shape and unexpected POST failure returning `500`. Syntax verification can still be done with `python -m py_compile`; full unittest execution requires Flask and mysql-connector in the local Python environment.
- Blockers: Docker daemon access is unavailable in this environment, and the local Python environment may not have backend Python dependencies installed.
- Next suggested action: Run backend unittests in a dependency-ready environment, then smoke test the live API with at least one student enrolled in more than one course.

- Date: 2026-04-10
- Jira: Backend enrollment write path
- Team: Backend
- Author: Codex
- Summary: Extended the normalized-schema write path by allowing `POST /api/students` to accept an optional `courseId`, returning enrollment-style create responses, and adding `POST /api/students/<studentId>/enrollments` for enrolling an existing student into another course with duplicate-enrollment protection and student/course existence checks.
- Files changed: `backend/app/validators.py`, `backend/app/services/student_service.py`, `backend/app/controllers/student_controller.py`, `backend/app/routes/students.py`, `backend/tests/test_api.py`, `backend/tests/test_student_service.py`, `backend/README.md`, `README.md`, `docs/ARCHITECTURE_DECISIONS.md`, `docs/DEV_LOG.md`, `docs/TEAM_HANDOFF.md`
- Verification: Installed backend dependencies from `backend/requirements.txt` and ran `python -m unittest discover -s backend/tests -v` successfully with 25 passing tests. Coverage now includes create-student with default and explicit course IDs, new enrollment writes, duplicate enrollment protection, multi-enrollment reads, and per-course averages.
- Blockers: No live Docker smoke test was run in this environment after the write-path extension.
- Next suggested action: Run `make reset-db && make up`, then manually POST one extra enrollment for a seeded student and confirm the list and average endpoints update as expected.
