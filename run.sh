#!/usr/bin/env bash
# run.sh - Quick launcher for Chrome bot
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

# Allow local connections for display automation
xhost +local: >/dev/null 2>&1 || true

python3 "$DIR/main.py" "$@"
