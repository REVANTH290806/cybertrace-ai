#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "===================================================="
echo "    Starting CyberTrace AI Platform (SIH26184)      "
echo "===================================================="

# Kill any existing instances on ports 8000 & 3000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

echo "1. Starting FastAPI Backend on http://127.0.0.1:8000..."
cd "$DIR"
"$DIR/backend/venv/bin/uvicorn" backend.app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "2. Starting Vite Frontend on http://127.0.0.1:3000..."
cd "$DIR/frontend"
npm run dev -- --host 127.0.0.1 --port 3000 &
FRONTEND_PID=$!

echo ""
echo "===================================================="
echo " CyberTrace AI is running!"
echo " Frontend URL: http://127.0.0.1:3000"
echo " Backend API:  http://127.0.0.1:8000"
echo " Demo User:    demo_officer / CyberTrace@123"
echo "===================================================="
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit 0" INT TERM
wait
