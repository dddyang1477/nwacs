@echo off
chcp 65001 >nul
title NWACS Creative Workbench

cd /d "%~dp0"

echo.
echo ============================================================
echo           NWACS Creative Workbench
echo ============================================================
echo.
echo  1. Start Full System
echo  2. Focus Writing Mode
echo  3. Plot Designer
echo  4. Configuration
echo  0. Exit
echo.

set /p choice=Enter choice [0-4]:

if "%choice%"=="1" py main.py
if "%choice%"=="2" py src/core/writing_mode.py
if "%choice%"=="3" py src/core/plot_designer.py
if "%choice%"=="4" py config_tool.py
if "%choice%"=="0" exit

pause
