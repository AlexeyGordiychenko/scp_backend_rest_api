#!/bin/bash
set -e

# Run Alembic migrations
alembic upgrade head

# Run tests
sh -c "python -m pytest -s -vv"
