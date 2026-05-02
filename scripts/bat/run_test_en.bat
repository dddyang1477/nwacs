@echo off
chcp 65001 >nul
echo ========================================
echo NWACS Test Script
echo ========================================
echo Current directory: %CD%
echo.
echo 1. Checking Python version...
python --version
echo.
echo 2. Running test script...
python test_output.py
echo.
echo 3. Done
echo ========================================
pause