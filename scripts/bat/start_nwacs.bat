@echo off
chcp 65001 >nul
title NWACS 飞书集成启动器
echo.
echo ========================================
echo    NWACS 飞书集成启动器
echo ========================================
echo.
echo [1] 启动飞书指令服务器
echo [2] 启动NWACS学习系统
echo [3] 发送测试消息到飞书
echo [4] 退出
echo.
set /p choice=请选择 (1-4):

if "%choice%"=="1" goto server
if "%choice%"=="2" goto learning
if "%choice%"=="3" goto test
if "%choice%"=="4" goto end

:server
echo.
echo ========================================
echo 启动NWACS飞书指令服务器...
echo ========================================
py feishu_server_v2.py
pause
goto end

:learning
echo.
echo ========================================
echo 启动NWACS学习系统...
echo ========================================
py start_auto_learn.py
pause
goto end

:test
echo.
echo ========================================
echo 发送测试消息...
echo ========================================
py feishu_simple_test.py
pause
goto end

:end
echo.
echo 再见！
