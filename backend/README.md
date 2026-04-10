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

| Method | Path                    | Description                                       |
| ------ | ----------------------- | ------------------------------------------------- |
| GET    | `/health`               | Returns `{"status":"ok","service":"backend"}`      |
| GET    | `/api/students`         | All students sorted by `studentId` ASC             |
| GET    | `/api/students/average` | Average course score: `{"averageScore": 85.45}`    |

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
```
