@echo off
chcp 65001 >nul
title NWACS 飞书指令服务器
echo ========================================
echo  NWACS 飞书指令服务器
echo ========================================
echo.
cd /d "%~dp0"
python feishu_command_server.py
pause
