#!/bin/bash
set -e

# Run Alembic migrations
alembic upgrade head

# Run tests
python -m pytest -s -vv
