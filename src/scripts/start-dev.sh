#!/bin/bash
set -e

# Run Alembic migrations
alembic upgrade head

# Start the Uvicorn server
exec uvicorn shopAPI.server:app --reload --host ${APP_HOST} --port ${APP_PORT}