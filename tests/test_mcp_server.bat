@echo off
cd /d "e:\Program Files (x86)\Trae CN\github\NWACS"
echo {"action": "describe"} | python mcp_server.py
pause