#!/bin/bash
echo "Starting Weather Station Server..."
# Navigate to where main.py is importable as backend.main
# Since we are in /app and backend code is in /app/backend, we run from /app
uvicorn backend.main:app --host 0.0.0.0 --port 80
