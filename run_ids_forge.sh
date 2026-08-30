#!/bin/bash
echo "============================================================"
echo "  IDS Forge ⚒️ - Hybrid Intrusion Detection System"
echo "  Author: R.M.L.S.B. Wijerathna (Student ID: 14519)"
echo "  Degree: BSc (Hons) in Computer Networks & Cyber Security"
echo "============================================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

if command -v python3 &> /dev/null; then
    PY_CMD="python3"
elif command -v python &> /dev/null; then
    PY_CMD="python"
else
    echo "[ERROR] Python 3 is not installed!"
    exit 1
fi

echo "[*] Installing required dependencies..."
$PY_CMD -m pip install -r requirements.txt

echo "[*] Starting IDS Forge Web Application..."
$PY_CMD -m streamlit run app.py
