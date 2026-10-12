@echo off
cd /d "%~dp0\.."

echo Starting shell emulator on Windows...
py main.py --vfs "vfs" --script "scripts\startup.txt"

pause