@echo off
echo ============================================================
echo   IDS Forge ⚒️ - Hybrid Intrusion Detection System
echo   Author: R.M.L.S.B. Wijerathna (Student ID: 14519)
echo   Degree: BSc (Hons) in Computer Networks & Cyber Security
echo ============================================================
echo.

cd /d "%~dp0"

echo [*] Checking Python environment...
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=py
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PY_CMD=python
    ) else (
        echo [ERROR] Python is not installed or not found in system PATH.
        echo Please install Python 3.10+ from https://www.python.org/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

echo [+] Found Python launcher: %PY_CMD%
echo [*] Installing required dependencies from requirements.txt...
%PY_CMD% -m pip install -r requirements.txt

echo.
echo [*] Starting IDS Forge Web Application...
%PY_CMD% -m streamlit run app.py

pause
