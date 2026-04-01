#!/usr/bin/env bash
set -e
[ -f .env ] || cp .env.example .env
docker compose --profile scaffold up --build -d
