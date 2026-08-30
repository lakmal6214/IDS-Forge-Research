@echo off
echo ============================================================
echo   IDS Forge - Hybrid Intrusion Detection System
echo   Author: R.M.L.S.B. Wijerathna (Student ID: 14519)
echo   Degree: BSc (Hons) in Computer Networks and Cyber Security
echo ============================================================
echo.

cd /d "%~dp0"

echo [*] Checking Python environment...

if exist ".venv\Scripts\python.exe" (
    set "PY_CMD=.venv\Scripts\python.exe"
    goto FOUND_PY
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=py"
    goto FOUND_PY
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=python"
    goto FOUND_PY
)

echo [ERROR] Python is not installed or not found in system PATH!
echo Please install Python 3.10+ from https://www.python.org/
echo Make sure to check "Add Python to PATH" during installation.
pause
exit /b 1

:FOUND_PY
echo [+] Using Python executable: %PY_CMD%
echo [*] Installing / verifying dependencies...
%PY_CMD% -m pip install -r requirements.txt

echo.
echo [*] Launching IDS Forge Interactive Web Application...
%PY_CMD% -m streamlit run app.py

pause
