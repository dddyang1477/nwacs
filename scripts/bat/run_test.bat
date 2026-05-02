@echo off
chcp 65001 >nul
echo ========================================
echo Python测试脚本
echo ========================================
echo 当前目录: %CD%
echo 日期时间: %date% %time%
echo.
echo 1. 检查Python版本...
python --version
echo.
echo 2. 运行测试脚本...
python test_output.py
echo.
echo 3. 完成
echo ========================================
pause