@echo off
chcp 65001 >nul
title NWACS 自动空闲学习系统

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                                                              ║
echo  ║         NWACS 自动空闲学习监控器 启动器                      ║
echo  ║                                                              ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 正在启动自动学习监控器...
echo.
echo 功能说明：
echo   - 电脑空闲 10 分钟后自动启动联网学习
echo   - 学习间隔为 1 小时（避免过于频繁）
echo   - 按 Ctrl+C 可随时退出
echo.
echo  启动中...
echo.

python core\auto_idle_learning.py -t 600 -s core\comprehensive_learning.py

pause
