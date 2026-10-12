#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

echo "Starting shell emulator on Linux/macOS..."
python3 main.py --vfs "vfs" --script "scripts/startup.txt"