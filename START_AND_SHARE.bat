@echo off
REM Quick start script for sharing your app with LocalTunnel

echo.
echo ======================================
echo   Blood Group Detector - Local Sharing
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11.7+
    pause
    exit /b 1
)

REM Check if localtunnel is installed
lt --version >nul 2>&1
if errorlevel 1 (
    echo Installing LocalTunnel...
    call npm install -g localtunnel
    if errorlevel 1 (
        echo ERROR: Failed to install LocalTunnel
        echo Please run: npm install -g localtunnel
        pause
        exit /b 1
    )
)

echo.
echo Step 1: Starting Flask app on port 5000...
echo.
start cmd /k "python app.py"

timeout /t 3

echo.
echo Step 2: Starting LocalTunnel sharing...
echo.
echo Your app will be available at a URL shown below.
echo Copy the URL and share it with anyone!
echo.
echo Keep this window open while sharing.
echo.

lt --port 5000

pause
