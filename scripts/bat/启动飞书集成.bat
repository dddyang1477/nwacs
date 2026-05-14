@echo off
chcp 65001 >nul
title NWACS 飞书集成

echo.
echo ========================================
echo   📱 NWACS 飞书集成 - 完整实现
echo ========================================
echo.
echo [1] 测试飞书连接（推荐先试）
echo [2] 查看系统状态
echo [3] 打开配置文件
echo [4] 退出
echo.

set /p choice=请选择功能 (1-4): 

if "%choice%"=="1" goto test
if "%choice%"=="2" goto status
if "%choice%"=="3" goto config
if "%choice%"=="4" goto end

:invalid
echo.
echo 无效选项，请重新选择！
pause
goto start

:test
echo.
echo ========================================
echo   测试飞书连接
echo ========================================
echo.
cd /d "%~dp0"
python core/feishu/nwacs_feishu.py
pause
goto start

:status
echo.
echo ========================================
echo   查看系统状态
echo ========================================
echo.
cd /d "%~dp0"
python -c "from core.feishu.nwacs_feishu import NWACSFeishuIntegration; i=NWACSFeishuIntegration(); i.send_status_update()"
pause
goto start

:config
echo.
echo 正在打开配置文件...
notepad "%~dp0config\feishu_config.json"
echo.
echo 配置完成后请重新运行此脚本！
pause
goto start

:end
echo.
echo 再见！
pause
