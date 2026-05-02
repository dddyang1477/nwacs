@echo off
chcp 65001 >nul
title NWACS 团队协作演示

echo.
echo ========================================
echo   👥 NWACS团队协作系统演示
echo ========================================
echo.

cd /d "%~dp0"

python core/team_collaboration.py

echo.
pause
