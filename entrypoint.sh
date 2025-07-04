#!/bin/bash

echo "Start migration"

uv run alembic upgrade head

echo "Start server"

uv run uvicorn main:app --host 0.0.0.0 --port 8000