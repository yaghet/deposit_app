#!/bin/bash

set -e

echo
echo "======================================="
echo ">>> Start migration <<<"
echo "======================================="
echo

uv run alembic upgrade head

echo
echo
echo ">>> Migration completed <<<"
echo
echo

echo
echo "======================================="
echo ">>> Start server <<<"
echo "======================================="
echo

uv run uvicorn main:app --host 0.0.0.0 --port 8000