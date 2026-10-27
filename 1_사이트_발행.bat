@echo off
cd /d "%~dp0"
set PY=py
where py >nul 2>nul || set PY=python
%PY% build.py --publish
if "%1"=="auto" exit /b
echo.
echo Done. See logs\publish.log for details.
pause
