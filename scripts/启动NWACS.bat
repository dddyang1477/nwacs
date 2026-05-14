@echo off
chcp 65001 > nul
cd /d "%~dp0"
title NWACS FINAL - AI写作助手
cls
echo ********************************************************************************
echo *                                                                               *
echo *     NWACS FINAL - Ultimate Novel Writing Assistant                           *
echo *     Version: 2026.05  |  One Version, All Features                           *
echo *                                                                               *
echo ********************************************************************************
echo.
echo Starting...
echo.
"C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe" NWACS_FINAL.py
pause
