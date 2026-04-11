# Backend - Python / Flask

## Stack

- **Language:** Python 3.12
- **Framework:** Flask 3.1
- **Database driver:** mysql-connector-python
- **CORS:** flask-cors
- **Configuration:** python-dotenv + environment variables

## Project structure

```text
backend/
|-- Dockerfile
|-- README.md
|-- run.py
|-- tests/
|   |-- test_api.py
|   `-- test_student_service.py
`-- app/
    |-- __init__.py
    |-- config.py
    |-- db.py
    |-- validators.py
    |-- controllers/
    |   `-- student_controller.py
    |-- routes/
    |   |-- health.py
    |   `-- students.py
    `-- services/
        `-- student_service.py
```

## API endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/health` | Returns `{"status":"ok","service":"backend"}` |
| GET | `/api/students` | Returns student-course enrollment records sorted by `studentId` ascending |
| POST | `/api/students` | Validates and creates a new student record |
| POST | `/api/students/<studentId>/enrollments` | Enrolls an existing student into another course |
| GET | `/api/students/average` | Returns average score grouped by course |

### `GET /api/students` response shape

```json
[
  {
    "studentId": 1,
    "firstName": "Alex",
    "middleName": null,
    "lastName": "Carter",
    "courseId": 1,
    "courseName": "Course Management",
    "score": 86.5
  },
  {
    "studentId": 1,
    "firstName": "Alex",
    "middleName": null,
    "lastName": "Carter",
    "courseId": 2,
    "courseName": "Database Systems",
    "score": 91.0
  }
]
```

The response is an enrollment list, not a collapsed one-row-per-student view. If a student has multiple course enrollments, multiple records are returned for that student. The list is ordered by `studentId` ascending and then `courseId` ascending.

Empty result returns `[]`.

### `POST /api/students` request body

```json
{
  "studentId": 6,
  "firstName": "Alex",
  "middleName": null,
  "lastName": "Carter",
  "courseId": 2,
  "score": 86.5
}
```

Field rules:
- `studentId` - required integer, unique, between `1` and `10`
- `firstName` / `lastName` - required non-empty string, letters/spaces/hyphens/apostrophes only, max 50 chars
- `middleName` - optional string with the same format rules
- `courseId` - optional positive integer; when omitted, the backend uses the seeded default course (`courseId = 1`)
- `score` - required number between `0` and `100` inclusive

### `POST /api/students` responses

**201 Created**

```json
{
  "studentId": 6,
  "firstName": "Alex",
  "middleName": null,
  "lastName": "Carter",
  "courseId": 1,
  "courseName": "Course Management",
  "score": 86.5
}
```

**400 Bad Request** for validation failure

```json
{
  "error": "Validation failed.",
  "details": ["studentId must be between 1 and 10."]
}
```

**400 Bad Request** for non-JSON request body

```json
{
  "error": "Request body must be JSON."
}
```

**400 Bad Request** for malformed JSON

```json
{
  "error": "Request body contains malformed JSON."
}
```

**400 Bad Request** for valid JSON that is not an object

```json
{
  "error": "Request body must be a JSON object."
}
```

**400 Bad Request** for expected database constraint failures other than duplicate ID

```json
{
  "error": "Student data violates database constraints."
}
```

**409 Conflict** for duplicate `studentId`

```json
{
  "error": "studentId already exists."
}
```

### `POST /api/students/<studentId>/enrollments` request body

```json
{
  "courseId": 2,
  "score": 91.0
}
```

This endpoint adds another enrollment for an existing student. It requires:
- an existing `studentId` in the path
- an existing `courseId` in the body
- a unique `(studentId, courseId)` pair
- `score` between `0` and `100`

**201 Created**

```json
{
  "studentId": 1,
  "firstName": "Alex",
  "middleName": null,
  "lastName": "Carter",
  "courseId": 2,
  "courseName": "Database Systems",
  "score": 91.0
}
```

**404 Not Found** when the student or course does not exist

```json
{
  "error": "studentId does not exist."
}
```

**409 Conflict** for duplicate enrollment

```json
{
  "error": "Student is already enrolled in this course."
}
```

### `GET /api/students/average` response shape

```json
{
  "courseAverages": [
    {
      "courseId": 1,
      "courseName": "Course Management",
      "averageScore": 86.65,
      "enrollmentCount": 5
    }
  ]
}
```

This endpoint reports per-course averages across enrolled students. It does not assume one score per student.

When there are no enrollments yet: `{ "courseAverages": [] }`.

## Seed data

The active Docker-backed schema path uses `database/init/01_schema.sql` and `database/init/02_data.sql`.
Those files create and seed the `student_db` database using the `Students`, `Courses`, and `Enrollments` tables.

The active seed data initializes **5 sample students** with `studentId` values `1` through `5`.
This leaves `6` through `10` available for live insert demos.

The active seed file also creates one default course, `Course Management` (`courseId = 1`). `POST /api/students` uses that default course when `courseId` is omitted.
Fresh seed data includes only that one course by default, so additional multi-course demos require more `Courses` rows to exist.

## Running

```bash
# From the project root
make up
make logs
make down

# Verify backend is up
curl http://localhost:5000/health
curl http://localhost:5000/api/students
curl http://localhost:5000/api/students/average

# Submit a student record
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"studentId":6,"firstName":"Alex","middleName":null,"lastName":"Carter","score":86.5}'
```

## Testing

Run backend tests from the `backend/` directory:

```bash
python -m unittest discover -s tests
```

## Testing checklist (Docker)

1. `make reset-db && make up` - confirm the database loads 5 seeded students
2. `curl http://localhost:5000/health` - expect `{"status":"ok","service":"backend"}`
3. `curl http://localhost:5000/api/students` - expect a JSON array of enrollment records sorted by `studentId` ascending
4. `curl http://localhost:5000/api/students/average` - expect `{"courseAverages": [...]}` grouped by course
5. POST a valid student with `studentId` between `6` and `10` - expect **201**
6. POST a duplicate `studentId` - expect **409** `studentId already exists.`
7. POST an enrollment for an existing student and valid `courseId` - expect **201**
8. POST a duplicate enrollment for the same student/course - expect **409**
9. POST malformed JSON with `Content-Type: application/json` - expect **400** `Request body contains malformed JSON.`
10. POST a valid JSON array like `[]` - expect **400** `Request body must be a JSON object.`

Inactive legacy path:
- `database/init/001_create_schema.sql`
- `database/init/002_seed_data.sql`
- These files are no longer mounted by the active Docker Compose database setup.
