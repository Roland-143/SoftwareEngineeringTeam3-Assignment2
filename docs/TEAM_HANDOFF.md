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

- From team: Backend
- To team: Frontend, QA
- Jira: Backend initial setup
- What is complete: Flask backend project created with routes, controllers, services, DB module. Dockerfile replaced with Python 3.12. Backend starts by default with `make up`. Endpoints: `GET /health`, `GET /api/students`, `GET /api/students/average`. CORS enabled.
- What is not complete: POST endpoint for adding students. Input validation. Unit/integration tests. Error handling improvements.
- Important files: `backend/README.md`, `backend/run.py`, `backend/app/`, `docker-compose.yml`, `.env.example`.
- Commands to know: `make up` (start db + backend), `curl http://localhost:5000/health`, `curl http://localhost:5000/api/students`.
- Risks / assumptions: Historical note for this handoff entry only: at that time the backend was using `001_create_schema.sql` / `002_seed_data.sql` with `course_management`. This is superseded by the newer backend handoff entry below.
- Recommended next step: Frontend team can replace mock data with `fetch("http://localhost:5000/api/students")`. QA can verify endpoint responses match the documented contract.

- From team: Backend
- To team: Frontend, QA
- Jira: Backend API hardening
- What is complete: The active backend now uses `database/init/01_schema.sql` and `database/init/02_data.sql` with the `student_db` database. Backend queries and inserts were adapted to the `Students` and `Enrollments` tables while preserving the existing API shape. `POST /api/students` rejects non-JSON, malformed JSON, and non-object JSON bodies with clear 400 responses. Duplicate student IDs return 409. The active seed file now loads 5 deterministic rows with IDs 1 through 5 so IDs 6 through 10 remain available for live inserts. Backend-only unittest coverage was added for the main API paths and service-level sorting behavior.
- What is not complete: Live Docker smoke testing was not completed in this environment because Docker daemon access is unavailable here.
- Important files: `database/init/01_schema.sql`, `database/init/02_data.sql`, `docker-compose.yml`, `backend/app/services/student_service.py`, `backend/app/controllers/student_controller.py`, `backend/app/validators.py`, `backend/tests/`.
- Commands to know: `make reset-db`, `make up`, `curl http://localhost:5000/api/students`, `curl -X POST http://localhost:5000/api/students -H "Content-Type: application/json" -d '{"studentId":6,"firstName":"Alex","middleName":null,"lastName":"Carter","score":86.5}'`, `cd backend && python -m unittest discover -s tests`
- Risks / assumptions: The active backend DB path is `student_db` via `01_schema.sql` and `02_data.sql`. The older `001_create_schema.sql` / `002_seed_data.sql` files remain in the repo but are inactive because the active Docker Compose files mount only `01_schema.sql` and `02_data.sql`.
- Recommended next step: Run the backend unittest suite in a Python environment with backend dependencies installed, then do a short Docker smoke test covering GET endpoints plus POST inserts for student IDs 6 through 10.

- From team: Backend
- To team: Frontend, QA
- Jira: Backend normalized schema follow-up
- What is complete: `GET /api/students` is now documented and tested as an enrollment-record endpoint, so one student may appear more than once when they have multiple course enrollments. `GET /api/students/average` is documented and tested as a per-course average endpoint with a `courseAverages` list. The unexpected POST insert failure branch now has explicit API test coverage. Root/backend docs now match the active `student_db` setup and the active schema path of `01_schema.sql` / `02_data.sql`.
- What is not complete: Full runtime verification still depends on running the backend tests and a Docker smoke test in an environment with Docker and backend Python dependencies installed.
- Important files: `backend/app/services/student_service.py`, `backend/tests/test_api.py`, `backend/tests/test_student_service.py`, `backend/README.md`, `README.md`, `docs/ARCHITECTURE_DECISIONS.md`.
- Commands to know: `make reset-db`, `make up`, `curl http://localhost:5000/api/students`, `curl http://localhost:5000/api/students/average`, `cd backend && python -m unittest discover -s tests`
- Risks / assumptions: `POST /api/students` still creates the new student's first enrollment in the seeded default course because the request body contains one score but no course selector. Multi-course read behavior is supported by the normalized schema and read queries.
- Recommended next step: After the environment is up, add a second enrollment manually for one seeded student and verify that `/api/students` returns two records for that student and `/api/students/average` reflects course-specific averages correctly.

- From team: Backend
- To team: Frontend, QA
- Jira: Backend enrollment write path
- What is complete: `POST /api/students` now accepts an optional `courseId` and returns an enrollment-style response including `courseId` and `courseName`. A new `POST /api/students/<studentId>/enrollments` endpoint was added for enrolling an existing student into another course. The endpoint validates request JSON, checks that the student and course exist, rejects duplicate enrollments with 409, and keeps the normalized read endpoints aligned with real multi-course data.
- What is not complete: Live Docker smoke testing for the new enrollment write path was not run in this environment.
- Important files: `backend/app/validators.py`, `backend/app/services/student_service.py`, `backend/app/controllers/student_controller.py`, `backend/app/routes/students.py`, `backend/tests/test_api.py`, `backend/tests/test_student_service.py`, `backend/README.md`.
- Commands to know: `curl -X POST http://localhost:5000/api/students -H "Content-Type: application/json" -d '{"studentId":6,"firstName":"Alex","middleName":null,"lastName":"Carter","courseId":1,"score":86.5}'`, `curl -X POST http://localhost:5000/api/students/1/enrollments -H "Content-Type: application/json" -d '{"courseId":2,"score":91.0}'`
- Risks / assumptions: The seed data still creates only one default course. Additional course enrollments require valid `courseId` values to already exist in the `Courses` table.
- Recommended next step: In the live environment, insert at least one additional course, then POST an enrollment for an existing seeded student and verify the list and course-average endpoints reflect both courses correctly.
