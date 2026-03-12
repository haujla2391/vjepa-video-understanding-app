#!/usr/bin/env bash
set -euo pipefail  # exit on errors, undefined vars, pipe failures

echo "Starting Uvicorn on port $PORT..."
echo "Python version: $(python --version)"
echo "Current dir: $(pwd)"
ls -la

echo "Testing basic import before full startup..."
python -c "import uvicorn; print('Uvicorn imported OK')" || echo "Uvicorn import failed"

echo "Testing FastAPI import..."
python -c "from fastapi import FastAPI; print('FastAPI imported OK')" || echo "FastAPI import failed"

echo "Running Uvicorn with maximum verbosity..."
uvicorn backend.app:app \
    --host 0.0.0.0 \
    --port $PORT \
    --log-level trace \
    --reload false \
    --no-access-log \
    --timeout-keep-alive 120

echo "Uvicorn exited with code $?"