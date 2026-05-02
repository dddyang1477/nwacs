@echo off
chcp 65001 >nul
title NWACS v7.0 超级启动器

echo.
echo ========================================
echo   🎭 NWACS v7.0 超级启动器
echo   一键启动所有功能
echo ========================================
echo.

cd /d "%~dp0"

python core/nwacs_super_launcher.py

pause
