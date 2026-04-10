# Course Management Database (MySQL + Docker + CLI)

## Overview

This project implements the database component of a course management system. It stores student information, course data, and scores, and provides queries for sorting and calculating averages.

The database is deployed using Docker and can be fully managed from the terminal.

---

## Technologies Used

* MySQL 8.0.45
* Docker (Compose v2)
* Ubuntu (CLI)
* GitHub (version control)

---

## Structure

```text
database/
│
├── docker-compose.yml
├── queries.sql
│
└── init/
    ├── 01_schema.sql
    └── 02_data.sql
```

> Note: Only files inside `init/` are automatically executed by Docker during initialization.

---

## File Descriptions

* `01_schema.sql` → creates database and tables
* `02_data.sql` → inserts sample data
* `queries.sql` → contains queries for sorting and averages
* `docker-compose.yml` → runs MySQL container
* `init/` → automatically initializes the database on first run

---

## Initialization Order

Docker executes SQL files in alphabetical order:

```
01_schema.sql → runs first (creates tables)
02_data.sql   → runs second (inserts data)
```

If this order is incorrect, the database will fail to initialize.

---

## Setup Instructions (Terminal)

### 1. Navigate to database folder

```bash
cd path/to/repository/database
```

---

### 2. Start the database (clean setup)

```bash
docker compose down -v
docker compose up -d
```

This ensures:

* a fresh database
* initialization scripts are executed

---

### 3. Verify container is running

```bash
docker ps
```

Expected output includes:

```
student_db   mysql:8.0   ...   0.0.0.0:3307->3306
```

---

### 4. Connect to the database (CLI)

```bash
mysql -h 127.0.0.1 -P 3307 -u root -p
```

Password:

```
password
```

---

### 5. Verify database setup

```sql
USE student_db;
SHOW TABLES;
```

Expected tables:

```
Students
Courses
Enrollments
```

---

### 6. View sample data

```sql
SELECT * FROM Students;
SELECT * FROM Courses;
SELECT * FROM Enrollments;
```

---

### 7. Run queries (optional)

```bash
mysql -h 127.0.0.1 -P 3307 -u root -p student_db < queries.sql
```

---

## Troubleshooting

### Tables are missing

```bash
docker compose down -v
docker compose up -d
```

---

### Tables don’t exist during initialization

Ensure file names are:

```
01_schema.sql
02_data.sql
```

---

### Port already in use

Change the port in `docker-compose.yml` (e.g., 3307)

---

### Check logs

```bash
docker logs student_db
```

---

## Notes

* The database is initialized automatically using the `init/` folder.
* Initialization only happens on first container creation.
* The `queries.sql` file is used for testing and backend integration.
* The average score is calculated using SQL `AVG()`.

Backend systems should connect using:

```
Host: 127.0.0.1
Port: 3307
```

---

## Author

Zachary Best
