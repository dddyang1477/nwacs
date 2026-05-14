@echo off
echo ========================================
echo NWACS DeepSeek 学习引擎 - 测试版本
echo ========================================
echo.

cd /d "%~dp0"
echo 当前目录: %CD%
echo.

echo 正在运行Python脚本...
echo.
python run_learning_test.py

echo.
echo ========================================
echo 脚本执行完成
echo ========================================
pause
