@echo off
chcp 65001 >nul
title NWACS全面检测和修复工具

echo.
echo ========================================
echo   🔍 NWACS全面检测和修复工具
echo ========================================
echo.
echo 1. 快速检测（编码+语法）
echo 2. 完整检测（包括DeepSeek分析）
echo 3. 退出
echo.
set /p choice="请选择: "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto full
if "%choice%"=="3" goto end

:invalid
echo.
echo 无效选项
pause
goto end

:quick
echo.
echo ========================================
echo   🚀 开始快速检测
echo ========================================
echo.
cd /d "%~dp0"
python core\nwacs_diagnostic.py --quick --api-key sk-f3246fbd1eef446e9a11d78efefd9bba
pause
goto end

:full
echo.
echo ========================================
echo   🚀 开始完整检测（DeepSeek分析）
echo ========================================
echo.
cd /d "%~dp0"
python core\nwacs_diagnostic.py --full --api-key sk-f3246fbd1eef446e9a11d78efefd9bba
pause
goto end

:end
echo.
echo 再见！
timeout /t 3
