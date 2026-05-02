@echo off
chcp 65001 >nul
echo ========================================
echo  NWACS 飞书指令服务器
echo ========================================
echo.
cd /d "%~dp0"
echo 当前目录: %CD%
echo.
python feishu_command_server.py
echo.
pause
