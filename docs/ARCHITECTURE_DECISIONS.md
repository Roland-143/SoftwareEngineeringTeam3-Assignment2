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

- ---

- Date: 2026-04-10
- Jira: Backend initial setup
- Team: Backend
- Decision: Backend stack is Python 3.12 / Flask 3.1 with mysql-connector-python, flask-cors, and python-dotenv. Backend service is no longer a scaffold placeholder and starts by default with Docker Compose.
- Reason: Flask is lightweight, well-documented, and easy for team members and instructors to understand. mysql-connector-python is the official Oracle-maintained MySQL driver, avoiding C-library compilation issues in Docker. flask-cors enables frontend integration across different ports. python-dotenv loads environment variables for local development.
- Alternatives considered: FastAPI (more complex async patterns not needed for this scope), Django (too heavyweight for a simple API), Express/Node.js (team chose Python).
- Impact on other teams: Frontend should call `GET /api/students` (port 5000) for student data and `GET /api/students/average` for score averages. CORS is enabled. Field names are camelCase.

- ---

- Date: 2026-04-06
- Jira: Frontend initial planning
- Team: Frontend
- Decision: The frontend will initially be planned as a simple React-based interface with 2 required pages: a Student Entry page and a Student Records page. An optional Home/Landing page may be added later only if time allows and the required flow is already complete.
- Reason: This approach keeps the frontend aligned with the assignment scope while making the UI easier to build, test, and demonstrate. The Student Entry page will handle input and validation for student data, and the Student Records page will display stored records in ascending order by student ID along with the average score. Keeping the design to 2 main pages reduces unnecessary complexity and supports a stable implementation using HTML, CSS, and JavaScript React.
- Alternatives considered: A single-page interface containing both the form and records view was considered for maximum simplicity. A 3-page structure with a dedicated Home/Landing page was also considered for a cleaner demo flow. The team chose the 2-page structure as the best balance between simplicity, usability, and presentation quality.
- Impact on other teams: Backend should expose endpoints needed for submitting student records and retrieving sorted records plus average data. Database team should ensure the schema supports first name, middle name, last name, student ID, and course score. QA can prepare checks around required fields, student ID range `1..10`, score range `0..100`, sorted display by student ID ascending, and average-score display.

- ---

- Date: 2026-04-10
- Jira: Backend normalized schema alignment
- Team: Backend
- Decision: The active backend database path uses `database/init/01_schema.sql` and `database/init/02_data.sql` with the `student_db` database. The backend treats `Students`, `Courses`, and `Enrollments` as the source of truth. `GET /api/students` returns enrollment records ordered by `studentId` and `courseId`, and `GET /api/students/average` returns per-course averages instead of assuming one score per student.
- Reason: The normalized schema allows one student to have multiple course enrollments. The backend needed to reflect that structure truthfully instead of flattening data into a one-enrollment-per-student assumption.
- Alternatives considered: Keeping the older `001_create_schema.sql` / `002_seed_data.sql` single-table path active; collapsing multiple enrollments into one API row per student; returning a single global average that hides per-course differences.
- Impact on other teams: Frontend and QA should treat `/api/students` as an enrollment list that may contain multiple records per student and `/api/students/average` as a course-average response with `courseAverages[]`. Docker/runtime setup should use `student_db` only.

- ---

- Date: 2026-04-10
- Jira: Backend enrollment write path
- Team: Backend
- Decision: `POST /api/students` remains the endpoint for creating a brand-new student, but now accepts an optional `courseId` for the student's first enrollment. A minimal `POST /api/students/<studentId>/enrollments` endpoint was added so an existing student can be enrolled into another course without changing the schema or broadening the API beyond assignment needs.
- Reason: The normalized schema supports multiple courses per student. The read path already reflected that, so the write path needed one small extension to stop forcing the backend into a single-enrollment assumption.
- Alternatives considered: Leaving writes limited to one default course only; replacing the student-create endpoint with a broader enrollment-first API; adding a larger course-management API surface.
- Impact on other teams: Frontend and QA can now create a student with an optional first course and then add further enrollments for the same student. Create/enrollment responses now use the same enrollment-style fields as `GET /api/students`.
