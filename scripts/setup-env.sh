#!/usr/bin/env bash
set -e
if [ -f .env ]; then
  echo ".env already exists"
else
  cp .env.example .env
  echo "Created .env from .env.example"
fi
