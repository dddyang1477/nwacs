@echo off
chcp 65001 >nul
title NWACS 微信集成 - 概念验证

echo.
echo ========================================
echo   📱 NWACS 微信集成
echo ========================================
echo.
echo [1] 交互式演示（模拟微信）
echo [2] 查看配置说明
echo [3] 配置企业微信机器人
echo [4] 退出
echo.

set /p choice=请选择功能 (1-4): 

if "%choice%"=="1" goto demo
if "%choice%"=="2" goto help
if "%choice%"=="3" goto config
if "%choice%"=="4" goto end

:invalid
echo.
echo 无效选项，请重新选择！
pause
goto start

:demo
echo.
echo ========================================
echo   交互式演示模式
echo ========================================
echo.
cd /d "%~dp0"
python core/wechat/nwacs_wechat.py
pause
goto start

:help
echo.
echo ========================================
echo   配置说明
echo ========================================
echo.
echo 方案一：企业微信机器人（推荐）
echo   1. 在企业微信群添加自定义机器人
echo   2. 获取webhook_url
echo   3. 填入 config/wechat_config.json
echo.
echo 方案二：个人微信（可选）
echo   1. 使用itchat库
echo   2. 有一定封号风险
echo.
echo 当前配置文件位置：
echo   %~dp0config\wechat_config.json
echo.
pause
goto start

:config
echo.
echo 正在打开配置文件...
notepad "%~dp0config\wechat_config.json"
echo.
echo 配置完成后请重新运行此脚本！
pause
goto start

:end
echo.
echo 再见！
pause
