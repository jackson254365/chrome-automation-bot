@echo off
REM run.bat - Windows Quick Launcher for Chrome Bot
title Chrome Automation Bot

echo ========================================================
echo        Chrome Automation Bot (Windows Launcher)
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo and ensure "Add Python to PATH" is checked during setup.
    pause
    exit /b 1
)

REM Check and install dependencies if needed
echo Checking Python dependencies...
python -c "import selenium, webdriver_manager, pyautogui" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    pip install -r "%~dp0requirements.txt"
)

echo Starting Bot...
echo.
python "%~dp0main.py" %*

pause
