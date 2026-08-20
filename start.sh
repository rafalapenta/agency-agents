#!/usr/bin/env bash
set -euo pipefail

echo "Starting Agentic OS Dashboard..."
echo ""

# Check if server.py exists
if [ ! -f server.py ]; then
    echo "ERROR: server.py not found. Are you in the right directory?"
    exit 1
fi

# Check virtual environment
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Run ./install.sh first."
    exit 1
fi

# Use venv Python directly (no shell activation needed)
PYTHON="$VENV_DIR/bin/python3"

# Ensure deps are up to date
UV="bin/uv"
if [ -x "$UV" ]; then
    "$UV" pip install --python "$PYTHON" -r requirements.txt --quiet
else
    "$PYTHON" -m pip install -r requirements.txt --quiet
fi

# Get port from settings or default
PORT=8080
PORT=$("$PYTHON" -c "import json; f=open('data/settings.json'); d=json.load(f); print(d.get('dashboard',{}).get('port',8080)); f.close()" 2>/dev/null || echo "8080")

echo "Dashboard: http://127.0.0.1:${PORT}"
echo "Press Ctrl+C to stop"
echo ""

# Kill any stale process still bound to the port (from a crashed/previous run)
if command -v lsof &>/dev/null; then
    PIDS=$(lsof -ti:"${PORT}" 2>/dev/null || true)
    if [ -n "${PIDS}" ]; then
        echo "Port ${PORT} in use — stopping stale process(es): ${PIDS}"
        kill -9 ${PIDS} 2>/dev/null || true
        sleep 1
    fi
fi

# Start server using venv Python
"$PYTHON" server.py --port "${PORT}"
