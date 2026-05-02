@echo off
chcp 65001 >nul
echo ========================================
echo NWACS Feishu Command Server
echo ========================================
cd /d "%~dp0"
py feishu_command_server.py
pause