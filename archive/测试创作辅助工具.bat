@echo off
chcp 65001 >nul
echo.
echo ╔========================================================╗
echo ║         NWACS 创作辅助工具测试                          ║
echo ╚========================================================╝
echo.

cd /d "%~dp0"

echo 正在启动测试程序...
echo.

python test_writing_assistant.py

echo.
echo 测试完成！按任意键退出...
pause >nul
