# Course Project 2 Repository Guide

This repository now contains the active backend implementation for the CS 41600 Course Project 2 team plus the frontend project area.
It started as a shared skeleton, but the backend stack and database path are now implemented and documented.

## Assignment Scope (Summary)

Build a small course-management website that:
- accepts student name, student ID, and course score input
- stores data in MySQL
- displays stored records in ascending order
- displays score averages for the class data stored in MySQL

## Current Repository State

- Active database bootstrap uses `database/init/01_schema.sql` and `database/init/02_data.sql`.
- The active database is `student_db`.
- The backend is implemented with Flask and starts by default with Docker Compose.
- The backend API exposes `GET /health`, `GET /api/students`, `POST /api/students`, `POST /api/students/<studentId>/enrollments`, and `GET /api/students/average`.
- The active seed data loads 5 demo students with unique `studentId` values `1` through `5`, leaving `6` through `10` available for live inserts.
- The legacy `001_create_schema.sql` / `002_seed_data.sql` files remain in the repo for reference only and are not mounted by the active Compose setup.

## Repository Layout

- `backend/`: active Flask backend service and backend tests
- `frontend/`: frontend project area
- `database/init/`: active MySQL schema and seed SQL
- `docs/`: scope, architecture decisions, dev log, handoff notes, and AI/dev workflow
- `scripts/`: helper shell scripts for Docker workflow
- `.github/pull_request_template.md`: PR checklist/template

## Quick Start (Ubuntu/WSL Preferred)

1. Create local env file:
   - `cp .env.example .env`
2. Set local values in `.env`:
   - `MYSQL_ROOT_PASSWORD`
   - `APP_DB_PASSWORD`
3. Start the active backend stack:
   - `docker compose up --build -d`
4. Optional: start the scaffold frontend container too:
   - `docker compose --profile scaffold up --build -d`
5. Check status/logs:
   - `docker compose ps`
   - `docker compose logs -f --tail=100`
6. Stop services:
   - `docker compose down`

Makefile shortcuts:
- `make up`
- `make down`
- `make logs`
- `make reset-db`
- `make ps`

## Environment Rules

- Commit `.env.example`.
- Never commit `.env` with real secrets.
- Keep placeholders in `.env.example` non-sensitive.

## Team Workflow Requirements

Before starting any work:
1. Read `README.md`
2. Read `docs/PROJECT_SCOPE.md`
3. Read `docs/AI_AND_DEV_INSTRUCTIONS.md`
4. Read `docs/ARCHITECTURE_DECISIONS.md`
5. Read `docs/DEV_LOG.md`
6. Work from the assigned Jira issue

Every PR should update documentation as needed:
- AI will do most of this :) 
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`
- `docs/ARCHITECTURE_DECISIONS.md` (if a decision changes)
- `README.md` (if setup/workflow changes)

## Active Backend Notes

- Active schema path: `database/init/01_schema.sql` and `database/init/02_data.sql`
- Active DB name: `student_db`
- `studentId` values are unique and limited to `1..10`
- `GET /api/students` returns student-course enrollment records sorted by `studentId`
- `GET /api/students/average` returns average scores grouped by course
- `POST /api/students` can use an optional `courseId`; if omitted, the default seeded course is used
- `POST /api/students/<studentId>/enrollments` adds another course enrollment for an existing student
- Student create/enrollment endpoints reject non-JSON, malformed JSON, and valid JSON that is not an object
