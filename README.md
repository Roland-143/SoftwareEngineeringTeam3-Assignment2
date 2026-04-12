# Course Project 2 Repository Guide

This repository contains a course-management application for CS 41600 Project 2:
- MySQL database (Docker)
- Flask backend API (Docker)
- React frontend (run locally with Vite)

## Assignment Scope (Summary)

Build a small course-management website that:
- accepts student name, student ID, and course score input
- stores data in MySQL
- displays records in ascending order
- displays score averages

## Current Implementation State

- Active schema/init files: `database/init/01_schema.sql` and `database/init/02_data.sql`
- Active database: `student_db`
- Backend API is implemented and starts by default in Docker Compose
- Frontend is implemented and should be run locally with `npm run dev`
- Legacy SQL files `001_create_schema.sql` and `002_seed_data.sql` remain for reference only (not mounted by active compose)

## Repository Layout

- `backend/`: Flask backend and tests
- `frontend/`: React + TypeScript + Vite app
- `database/init/`: active MySQL schema and seed SQL
- `docs/`: scope, architecture decisions, dev log, handoff notes
- `scripts/`: helper shell scripts for Docker workflows

## Prerequisites

- Docker Desktop (or Docker Engine + Compose v2)
- Git
- Node.js 20+ and npm (for local frontend run)

## Clone and Setup

1. Clone the repo:

```bash
git clone <your-repo-url>
cd SoftwareEngineeringTeam3-Assignment2
```

2. Create env file:

Linux/macOS/WSL:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

3. Edit `.env` and set at minimum:
- `MYSQL_ROOT_PASSWORD`
- `APP_DB_PASSWORD`

If local port `3306` is busy, change:
- `MYSQL_PORT=3307`

## Start the Backend + Database (Docker)

From repository root:

```bash
docker compose down -v
docker compose up --build -d
docker compose ps
```

Expected services:
- `course-project2-db-1` (healthy)
- `course-project2-backend-1` (up, port `5000`)

## Verify API is Running

If you are in `cmd`:

```cmd
curl http://localhost:5000/health
curl http://localhost:5000/api/students
curl http://localhost:5000/api/students/average
```

If you are in PowerShell:

```powershell
Invoke-RestMethod http://localhost:5000/health
Invoke-RestMethod http://localhost:5000/api/students
Invoke-RestMethod http://localhost:5000/api/students/average
```

## Run Frontend Locally

The compose `frontend` service is scaffold-only. Run the real frontend locally:

```bash
cd frontend
npm install
npm run dev
```

Open:
- `http://localhost:5173`

Frontend uses backend at `http://localhost:5000` by default.
To override, set `VITE_API_BASE_URL` in your frontend environment.

## Common Commands

From repository root:

```bash
docker compose up --build -d
docker compose down
docker compose down -v
docker compose logs -f --tail=100
docker compose ps
```

Makefile shortcuts (Linux/macOS/WSL with `make`):
- `make up`
- `make down`
- `make logs`
- `make reset-db`
- `make ps`

## Common Errors and Fixes

### 1) Docker daemon not running
Error example:
- `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`

Fix:
- Start Docker Desktop and wait for "Engine running"
- Then run `docker version` and confirm both Client and Server sections are present

### 2) MySQL port already in use
Error example:
- `bind: ... 0.0.0.0:3306 ... only one usage ...`

Fix:
- In `.env`, set `MYSQL_PORT=3307`
- Re-run:

```bash
docker compose down
docker compose up --build -d
```

### 3) `Invoke-RestMethod` not recognized
Cause:
- You are in `cmd`, not PowerShell

Fix:
- Use `curl` in `cmd`, or run PowerShell commands from PowerShell

### 4) `npm` blocked by PowerShell execution policy
Error example:
- `npm.ps1 cannot be loaded because running scripts is disabled`

Fix:
- Use `cmd` for npm commands:

```cmd
cmd /c npm install
cmd /c npm run dev
```

### 5) Frontend shows no data / cannot connect to backend
Checklist:
- `docker compose ps` shows backend up on `5000`
- `curl http://localhost:5000/health` returns JSON
- Frontend is running on `5173`
- API base URL points to `http://localhost:5000`

### 6) Need a clean DB reset after SQL changes

```bash
docker compose down -v
docker compose up --build -d
```

## API Endpoints (Summary)

- `GET /health`
- `GET /api/students`
- `POST /api/students`
- `POST /api/students/<studentId>/enrollments`
- `GET /api/students/average`

Notes:
- Student IDs are constrained to `1..10`
- Seed data uses IDs `1..5`; use `6..10` for easy demo inserts

## Team Workflow Requirements

Before starting work:
1. Read `README.md`
2. Read `docs/PROJECT_SCOPE.md`
3. Read `docs/AI_AND_DEV_INSTRUCTIONS.md`
4. Read `docs/ARCHITECTURE_DECISIONS.md`
5. Read `docs/DEV_LOG.md`
6. Work from assigned Jira issue

For each PR, update docs as needed:
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`
- `docs/ARCHITECTURE_DECISIONS.md` (if decisions changed)
- `README.md` (if setup/workflow changed)
