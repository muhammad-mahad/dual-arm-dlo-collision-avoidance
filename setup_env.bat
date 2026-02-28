@echo off
:: ============================================================
::  setup_env.bat  —  Windows
::  Usage: Double-click OR run from Command Prompt
:: ============================================================

setlocal enabledelayedexpansion

set VENV_NAME=venv
set SCRIPT_DIR=%~dp0
set REQUIREMENTS=%SCRIPT_DIR%requirements.txt

echo ============================================
echo   Dual-Arm DLO Demo — Environment Setup
echo ============================================

:: ── 1. Check Python ──────────────────────────────────────────
echo.
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ and add to PATH.
    pause & exit /b 1
)
python --version
python -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.10+ required.
    pause & exit /b 1
)
echo    OK

:: ── 2. Check requirements.txt exists ─────────────────────────
echo.
echo [2/5] Checking requirements.txt...
if not exist "%REQUIREMENTS%" (
    echo ERROR: requirements.txt not found at %REQUIREMENTS%
    pause & exit /b 1
)
echo    Found: %REQUIREMENTS%
echo    OK

:: ── 3. Create virtual environment ────────────────────────────
echo.
echo [3/5] Creating virtual environment '%VENV_NAME%'...
if exist "%SCRIPT_DIR%%VENV_NAME%" (
    echo    Removing existing '%VENV_NAME%\'...
    rmdir /s /q "%SCRIPT_DIR%%VENV_NAME%"
)
python -m venv "%SCRIPT_DIR%%VENV_NAME%"
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause & exit /b 1
)
call "%SCRIPT_DIR%%VENV_NAME%\Scripts\activate.bat"
echo    OK

:: ── 4. Upgrade pip and install from requirements.txt ─────────
echo.
echo [4/5] Installing from requirements.txt...
python -m pip install --upgrade pip --quiet
pip install -r "%REQUIREMENTS%"
if errorlevel 1 (
    echo ERROR: Installation failed.
    pause & exit /b 1
)
echo    OK

:: ── 5. Verify installed packages ─────────────────────────────
echo.
echo [5/5] Verifying installed packages...
pip list --format=columns
echo    OK

:: ── Done ─────────────────────────────────────────────────────
echo.
echo ============================================
echo   Setup complete!
echo ============================================
echo.
echo To activate in a new terminal:
echo    %VENV_NAME%\Scripts\activate.bat
echo.
echo To run the demo:
echo    cd simulation ^&^& python demo_pick_cube.py
echo.
pause
