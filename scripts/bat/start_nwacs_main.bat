@echo off
chcp 65001 >nul
title NWACS v7.0 启动器
echo.
echo  ================================================================
echo.
echo     _   _                     _____                     _
echo     ^\^ ^\^                   ^/  __^\\^                   ^(^)
echo    ^/ ^\^ ^\^   __   __   _ __^/ ^|^_^  ^\^^^__   __^| ^|^|_   _  ____
echo   ^/ ^\^ ^\^ ^/ ^  ^\^/  ^\^/ ^__^/ __^  ^/ __^ ^/ _` ^|^| ^| ^|^ ^| ^| ^|  _ ^^\  / __^| ^/ __^|
echo  ^/ ^_^ ^_^ ^/ ^_^  ^/ ^_^ ^\__ ^\__^\ ( (__^ ( (__^ ^| ^|^ ^|^ ^|^ ^|^ ^| ^|^ ^) ^\__ ^\
echo ^/_____/____/____/^____/^___/^|____/ ^\___^ ^\___^|_^|^/ ^|^|^_^|^_^^_^/^|____/^|___/
echo.
echo                      v7.0 智能协作生态系统
echo.
echo  ================================================================
echo.
echo [1] 启动飞书集成 (NWACS -^> 飞书 消息推送)
echo [2] 启动飞书指令服务器 (双向通信，需要ngrok)
echo [3] 启动自动学习系统
echo [4] 发送测试消息
echo [5] 查看系统状态
echo [6] 帮助
echo [7] 退出
echo.
echo  ================================================================
echo.

set /p choice=请选择 (1-7):

if "%choice%"=="1" goto server
if "%choice%"=="2" goto双向
if "%choice%"=="3" goto learning
if "%choice%"=="4" goto test
if "%choice%"=="5" goto status
if "%choice%"=="6" goto help
if "%choice%"=="7" goto end

:server
echo.
echo [启动飞书集成服务器...]
echo.
py feishu_server_v2.py
pause
goto end

:双向
echo.
echo [启动飞书双向通信服务器...]
echo [提示: 需要先安装并配置ngrok]
echo.
echo 1. 下载ngrok: https://ngrok.com/download
echo 2. 运行: ngrok http 8088
echo 3. 复制公网URL到飞书机器人配置
echo.
py feishu_server_v2.py
pause
goto end

:learning
echo.
echo [启动NWACS学习系统...]
echo.
py start_auto_learn.py
pause
goto end

:test
echo.
echo [发送测试消息到飞书...]
echo.
py feishu_simple_test.py
pause
goto end

:status
echo.
echo [查看系统状态...]
echo.
py -c "from core.service_orchestrator import orchestrator; print(orchestrator.get_status())"
pause
goto end

:help
echo.
echo  ================================================================
echo  NWACS v7.0 帮助信息
echo  ================================================================
echo.
echo  一、功能说明:
echo  - [1] 飞书集成: NWACS发送消息到飞书群
echo  - [2] 双向通信: 飞书发送指令到NWACS (需要ngrok)
echo  - [3] 自动学习: 空闲时自动学习知识库
echo  - [4] 测试消息: 发送测试消息到飞书
echo  - [5] 系统状态: 查看NWACS运行状态
echo.
echo  二、快速开始:
echo  1. 先运行 [4] 发送测试消息，确认飞书配置正确
echo  2. 运行 [1] 启动飞书集成
echo  3. 系统会自动推送学习完成通知到飞书
echo.
echo  三、配置双向通信:
echo  1. 下载安装ngrok
echo  2. 注册ngrok账号并获取token
echo  3. 运行: ngrok config add-authtoken YOUR_TOKEN
echo  4. 运行: ngrok http 8088
echo  5. 复制ngrok的URL到飞书机器人配置
echo  6. 运行 [2] 启动双向通信
echo.
echo  四、查看日志:
echo  - 日志目录: logs\
echo  - 学习报告: skills\level2\learnings\学习进化报告\
echo.
echo  ================================================================
pause
goto end

:end
echo.
echo 再见！NWACS v7.0
