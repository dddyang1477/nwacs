@echo off
chcp 65001 >nul
title NWACS v7.0 API服务

echo.
echo ========================================
echo   🚀 NWACS v7.0 API服务
echo   Web UI后端服务
echo ========================================
echo.

cd /d "%~dp0"

echo 📦 正在启动API服务...
echo.
echo 🌐 启动后访问: http://localhost:5000
echo 📚 API文档: http://localhost:5000/api/health
echo.
echo 按 Ctrl+C 停止服务
echo.

python core/api_server.py

pause
