@echo off
chcp 65001 >nul
title NWACS DeepSeek评测工具

echo.
echo ========================================
echo   🧠 NWACS DeepSeek评测工具
echo   使用DeepSeek对项目进行全面评测
echo ========================================
echo.

cd /d "%~dp0"

python core\nwacs_evaluator.py --api-key sk-f3246fbd1eef446e9a11d78efefd9bba

echo.
echo ========================================
echo   ✅ 评测完成！
echo ========================================
echo.
pause
