# Course Project 2 Repository Guide

This repository is a shared skeleton for the CS 41600 Course Project 2 team.
It is intentionally stack-neutral so frontend/backend teams can make a documented stack decision before implementation.

## Assignment Scope (Summary)

Build a small course-management website that:
- accepts student name, student ID, and course score input
- stores data in MySQL
- displays stored records in ascending order
- displays the average score for 20 students

## Current Repository State

- Database bootstrap is provided (`database/init/*.sql`).
- Backend and frontend folders are placeholders only.
- No backend or frontend language/framework is enforced yet.
- Docker Compose defaults to `db` only.
- Optional `scaffold` profile can start placeholder backend/frontend workspace containers.

## Repository Layout

- `backend/`: stack-neutral backend placeholder area
- `frontend/`: stack-neutral frontend placeholder area
- `database/init/`: starter schema and seed SQL
- `docs/`: scope, architecture decisions, dev log, handoff notes, and AI/dev workflow
- `scripts/`: helper shell scripts for Docker workflow
- `.github/pull_request_template.md`: PR checklist/template

## Quick Start (Ubuntu/WSL Preferred)
# Database needs to be initialized first #

1. Create local env file:
   - `cp .env.example .env`
2. Set local values in `.env`:
   - `MYSQL_ROOT_PASSWORD`
   - `APP_DB_PASSWORD`
3. Start database only:
   - `docker compose up --build -d`
4. Optional: start stack-neutral scaffold containers too:
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

## What To Do Once Stack Is Chosen

Backend team:
- replace `backend/Dockerfile`
- add backend runtime/dependency/source files
- document decision and migration plan in `docs/ARCHITECTURE_DECISIONS.md`

Frontend team:
- replace `frontend/Dockerfile`
- add frontend runtime/dependency/source files
- document decision and migration plan in `docs/ARCHITECTURE_DECISIONS.md`
