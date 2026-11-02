@echo off
chcp 65001 > nul
title Freelance Jobs Radar

echo =======================================================
echo   Freelance Jobs Radar - One-Click Launcher
echo =======================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.8+ and check "Add Python to PATH".
    pause
    exit /b 1
)

:: Run Radar
echo [*] Executing Freelance Jobs Radar...
echo.
python main.py

echo.
echo =======================================================
echo   Execution finished. Check data/latest_matches.md
echo =======================================================
pause
