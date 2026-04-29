@echo off
chcp 65001 >nul
title 添加学习标记

cd /d "e:\Program Files (x86)\Trae CN\github\NWACS"

echo =====================================
echo     为所有Skill添加学习标记
echo =====================================
echo.

C:\Users\Administrator\AppData\Local\Programs\Python\Launcher\py.exe setup_learning_markers.py

pause