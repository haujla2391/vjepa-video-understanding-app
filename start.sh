#!/usr/bin/env bash
set -e  # exit on any error

echo "Starting Uvicorn..."
echo "PORT is: $PORT"
echo "Current dir: $(pwd)"
ls -la

uvicorn backend.app:app \
    --host 0.0.0.0 \
    --port $PORT \
    --log-level debug \
    --no-access-log  # optional: reduce noise

echo "Uvicorn exited with code $?"