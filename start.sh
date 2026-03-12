#!/usr/bin/env bash
set -euo pipefail

echo "Starting Uvicorn on port $PORT..."
echo "Python version: $(python --version)"
echo "Current dir: $(pwd)"
ls -la

# Quick import tests
python -c "import uvicorn; print('Uvicorn imported OK')" || echo "Uvicorn import failed"
python -c "from fastapi import FastAPI; print('FastAPI imported OK')" || echo "FastAPI import failed"

echo "Launching Uvicorn..."

uvicorn backend.app:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --log-level trace \
    --no-access-log \
    --timeout-keep-alive 120

echo "Uvicorn exited with code $?"