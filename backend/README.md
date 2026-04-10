# Backend – Python / Flask

## Stack

- **Language:** Python 3.12
- **Framework:** Flask 3.1
- **Database driver:** mysql-connector-python
- **CORS:** flask-cors
- **Configuration:** python-dotenv + environment variables

## Project structure

```
backend/
├── Dockerfile
├── requirements.txt
├── run.py                          # Entry point
└── app/
    ├── __init__.py                 # Flask app factory
    ├── config.py                   # Reads env vars
    ├── db.py                       # MySQL connection pool
    ├── routes/
    │   ├── __init__.py
    │   ├── health.py               # GET /health
    │   └── students.py             # GET /api/students, GET /api/students/average
    ├── controllers/
    │   ├── __init__.py
    │   └── student_controller.py   # HTTP request/response logic
    └── services/
        ├── __init__.py
        └── student_service.py      # Business logic + SQL queries
```

## API endpoints

| Method | Path                    | Description                                               |
| ------ | ----------------------- | --------------------------------------------------------- |
| GET    | `/health`               | Returns `{"status":"ok","service":"backend"}`              |
| GET    | `/api/students`         | All students sorted by `studentId` ASC                    |
| POST   | `/api/students`         | Create a new student record                               |
| GET    | `/api/students/average` | Average course score and student count                    |

### `GET /api/students` response shape

```json
[
  {
    "studentId": 1,
    "firstName": "Alex",
    "middleName": null,
    "lastName": "Carter",
    "score": 86.5
  }
]
```

Empty table returns `[]`.

### `POST /api/students` request body

```json
{
  "studentId": 1,
  "firstName": "Alex",
  "middleName": null,
  "lastName": "Carter",
  "score": 86.5
}
```

Field rules:
- `studentId` – integer, 1–20, required
- `firstName` / `lastName` – non-empty string, letters/spaces/hyphens/apostrophes, max 50 chars, required
- `middleName` – same format, optional (`null` or omitted)
- `score` – number, 0–100 inclusive, required

**201 Created** (success):
```json
{
  "studentId": 1,
  "firstName": "Alex",
  "middleName": null,
  "lastName": "Carter",
  "score": 86.5
}
```

**400 Bad Request** (validation failure):
```json
{
  "error": "Validation failed.",
  "details": ["studentId must be between 1 and 20.", "score is required."]
}
```

### `GET /api/students/average` response shape

```json
{ "averageScore": 85.45, "count": 20 }
```

When the table is empty: `{ "averageScore": null, "count": 0 }`.

## Environment variables

| Variable      | Example             | Set by               |
| ------------- | ------------------- | -------------------- |
| `APP_ENV`     | `development`       | docker-compose       |
| `PORT`        | `5000`              | docker-compose       |
| `DB_HOST`     | `db`                | docker-compose       |
| `DB_PORT`     | `3306`              | docker-compose       |
| `DB_NAME`     | `course_management` | docker-compose       |
| `DB_USER`     | `studentapp`        | docker-compose       |
| `DB_PASSWORD` | *(from .env)*       | docker-compose       |

## Running

```bash
# From the project root (with docker-compose)
make up          # starts db + backend
make logs        # tail logs
make down        # stop everything

# Verify backend is up
curl http://localhost:5000/health
curl http://localhost:5000/api/students
curl http://localhost:5000/api/students/average

# Submit a student record
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"studentId":1,"firstName":"Alex","middleName":null,"lastName":"Carter","score":86.5}'
```

## Testing checklist (Docker)

1. `make up` – confirm both `db` and `backend` containers start without error
2. `curl http://localhost:5000/health` – expect `{"status":"ok","service":"backend"}`
3. `curl http://localhost:5000/api/students` – expect a JSON array, sorted by `studentId` ASC
4. `curl http://localhost:5000/api/students/average` – expect `{"averageScore": <float|null>, "count": <int>}`
5. POST a valid student (see command above) – expect **201** with the inserted record
6. POST with a missing `firstName` – expect **400** with `"details"` listing the error
7. POST with `studentId: 99` – expect **400** `studentId must be between 1 and 20`
8. POST with `score: 150` – expect **400** `score must be between 0 and 100`
9. POST with non-JSON body – expect **400** `Request body must be JSON`
10. `make reset-db && make up` – confirm seed data loads and GET /api/students returns 20 rows
