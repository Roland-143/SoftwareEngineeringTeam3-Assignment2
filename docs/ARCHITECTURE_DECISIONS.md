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
- Impact on other teams: Frontend should call `GET /api/students` (port 5000) for sorted student records and `GET /api/students/average` for average score. CORS is enabled. Field names are camelCase: studentId, firstName, middleName, lastName, score.

- ---

- Date: 2026-04-06
- Jira: Frontend initial planning
- Team: Frontend
- Decision: The frontend will initially be planned as a simple React-based interface with 2 required pages: a Student Entry page and a Student Records page. An optional Home/Landing page may be added later only if time allows and the required flow is already complete.
- Reason: This approach keeps the frontend aligned with the assignment scope while making the UI easier to build, test, and demonstrate. The Student Entry page will handle input and validation for student data, and the Student Records page will display stored records in ascending order by student ID along with the average score. Keeping the design to 2 main pages reduces unnecessary complexity and supports a stable implementation using HTML, CSS, and JavaScript React.
- Alternatives considered: A single-page interface containing both the form and records view was considered for maximum simplicity. A 3-page structure with a dedicated Home/Landing page was also considered for a cleaner demo flow. The team chose the 2-page structure as the best balance between simplicity, usability, and presentation quality.
- Impact on other teams: Backend should expose endpoints needed for submitting student records and retrieving sorted records plus average score. Database team should ensure the schema supports first name, middle name, last name, student ID, and course score. QA team can prepare validation and UI test cases around required field checks, student ID range 1–10, course score range 0–100, sorted display by student ID ascending, and average score display.
