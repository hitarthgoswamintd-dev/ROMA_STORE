@echo off
setlocal enableextensions

REM Check Python availability
where python >nul 2>&1
if %errorlevel% neq 0 (
  echo Python not found on PATH.
  echo Install Python 3.10+ from https://www.python.org/downloads/ and select "Add to PATH" during install.
  echo Alternatively, run with Docker: docker compose up --build
  pause
  exit /b 1
)

REM Create venv if missing
if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate

REM Upgrade pip and install deps
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Set env and run
set FLASK_ENV=development
if "%FLASK_PORT%"=="" set FLASK_PORT=5000

python app.py
