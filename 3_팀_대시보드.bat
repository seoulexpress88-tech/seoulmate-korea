@echo off
cd /d "%~dp0"
set PY=py
where py >nul 2>nul || set PY=python
start "" http://localhost:8790
%PY% ops/ops.py serve --port 8790
