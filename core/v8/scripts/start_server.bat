@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ============================================================
echo   NWACS 商用级写作工具 v10.0
echo ============================================================
echo.
echo 正在启动服务器...
echo.
python nwacs_server_v3.py
pause