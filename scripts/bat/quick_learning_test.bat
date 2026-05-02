@echo off
chcp 65001 >nul
echo ========================================
echo NWACS 快速学习测试
echo ========================================
cd /d "%~dp0"
python quick_learning_test.py
echo.
pause
