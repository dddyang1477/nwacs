@echo off
chcp 65001 >nul
title NWACS Config
py "%~dp0config_tool.py"
pause