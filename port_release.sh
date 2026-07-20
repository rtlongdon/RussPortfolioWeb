#!/bin/bash
# Frees port 8793 if a stalled dev server is still holding it.
PORT=8793

PID=$(powershell -NoProfile -Command "(Get-NetTCPConnection -LocalPort $PORT -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess)" 2>/dev/null | tr -d '\r')

if [ -z "$PID" ]; then
  echo "Port $PORT is not in use."
else
  echo "Port $PORT is held by PID $PID. Stopping it..."
  powershell -NoProfile -Command "Stop-Process -Id $PID -Force"
  echo "Done. Port $PORT is free."
fi

read -p "Press Enter to close..."
