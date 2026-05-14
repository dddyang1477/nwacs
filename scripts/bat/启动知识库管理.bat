@echo off
chcp 65001 >nul
title NWACS 用户知识库管理

echo.
echo ========================================
echo   📚 NWACS用户知识库管理系统
echo ========================================
echo.

cd /d "%~dp0"

python core/knowledge_base_manager.py

echo.
pause
