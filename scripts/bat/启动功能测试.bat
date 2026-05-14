@echo off
chcp 65001 >nul
title NWACS v7.0 功能测试

echo.
echo ========================================
echo   🧪 NWACS v7.0 快速功能测试
echo   验证系统所有功能是否正常
echo ========================================
echo.

cd /d "%~dp0"
python core/nwacs_functional_test.py

echo.
pause
