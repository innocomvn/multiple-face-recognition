@echo off
REM Face Recognition Attendance System - Quick Start Script for Windows

echo.
echo ========================================
echo   Face Recognition System - Starting
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\.installed" (
    echo.
    echo [INFO] Installing dependencies...
    echo This may take 5-10 minutes...
    pip install -r requirements.txt

    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )

    type nul > venv\.installed
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] Dependencies already installed
)

REM Create necessary directories
echo.
echo [INFO] Checking directories...
if not exist "Training images\" mkdir "Training images"
if not exist "Customer images\" mkdir "Customer images"
echo [OK] Directories ready

REM Start the application
echo.
echo ========================================
echo   Starting application...
echo ========================================
echo.
echo   Access at: http://localhost:5000
echo.
echo   Press Ctrl+C to stop
echo ========================================
echo.

python app_improved.py

pause
