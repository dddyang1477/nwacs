@echo off
chcp 65001 >nul
title NWACS 立即学习模式

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                                                              ║
echo  ║         NWACS 立即学习系统 v2.0                              ║
echo  ║                                                              ║
echo  ║         无需等待空闲，立即开始学习！                          ║
echo  ║                                                              ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 正在启动学习系统...
echo.

python "core\comprehensive_learning.py"

pause
