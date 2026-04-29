@echo off
chcp 65001 >nul
title 设置NWACS学习系统自动启动

echo.
echo =====================================
echo     设置NWACS学习系统自动启动
echo =====================================
echo.

set "regPath=HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
set "regName=NWACS_AutoLearning"
set "vbsPath=e:\Program Files (x86)\Trae CN\github\NWACS\start_learning_bg.vbs"

echo 正在设置注册表启动项...
echo.

reg add "%regPath%" /v "%regName%" /t REG_SZ /d "wscript.exe ""%vbsPath%""" /f

if %errorlevel% equ 0 (
    echo ✅ 成功设置自动启动！
    echo.
    echo 📋 设置信息：
    echo   注册表路径: %regPath%
    echo   启动项名称: %regName%
    echo   运行程序: wscript.exe "%vbsPath%"
    echo.
    echo 💡 学习系统将在下次登录时自动启动
    echo 💡 如需取消自动启动，请运行: setup_auto_startup_remove.bat
) else (
    echo ❌ 设置失败，请以管理员身份运行此脚本
)

echo.
pause