@echo off
REM ROMA Shopping Agent - Docker Startup Script
REM This script starts the application using Docker

echo.
echo ========================================
echo   ROMA Shopping Agent - Docker Startup
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not on PATH
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Docker...
docker --version
echo.

echo [2/3] Building and starting ROMA Shopping Agent...
echo.
docker compose up --build

echo.
echo ========================================
echo   Server stopped
echo ========================================
pause
