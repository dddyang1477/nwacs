@echo off
chcp 65001 >nul
echo.
echo ╔========================================================╗
echo ║           NWACS 系统优化功能演示                        ║
echo ╚========================================================╝
echo.

cd /d "%~dp0"

echo 正在启动演示程序...
echo.

python demo_optimizations.py

echo.
echo 演示完成！按任意键退出...
pause >nul
