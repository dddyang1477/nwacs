@echo off
chcp 65001 >nul
title NWACS v7.0 统一启动器

echo.
echo ========================================
echo   🎭 NWACS v7.0 统一启动器
echo   小说创作AI协作系统
echo ========================================
echo.

cd /d "%~dp0"

python core/nwacs_launcher.py

echo.
pause
