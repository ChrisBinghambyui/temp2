@echo off
REM ============================================================
REM LOADED BONES MULTIPLAYER SERVER LAUNCHER
REM This script starts ngrok and the Node.js server
REM ============================================================

setlocal enabledelayedexpansion

REM Check if ngrok exists
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] ngrok not found in PATH
    echo.
    echo Please install ngrok from https://ngrok.com/download
    echo Then add it to your system PATH or place ngrok.exe in this folder.
    echo.
    pause
    exit /b 1
)

REM Check if npm exists
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] npm not found. Please install Node.js from https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo LOADED BONES MULTIPLAYER SERVER LAUNCHER
echo ============================================================
echo.
echo Starting ngrok tunnel on port 3000...
echo.

REM Start ngrok in a new window
start "NGrok Tunnel" cmd /k ngrok http 3000

REM Wait for ngrok to initialize
timeout /t 3 /nobreak

echo.
echo Starting Node.js multiplayer server...
echo.

REM Start npm server
npm.cmd start

REM Keep window open if server crashes
pause
