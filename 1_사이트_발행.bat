@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=py
where py >nul 2>nul || set PY=python
%PY% build.py --publish
if "%1"=="auto" exit /b
echo.
echo 결과는 logs\publish.log 에도 기록돼요.
pause
