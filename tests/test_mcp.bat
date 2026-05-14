@echo off
cd /d "e:\Program Files (x86)\Trae CN\github\NWACS"
echo 正在测试MCP服务器...
echo {"action": "describe"} | python simple_mcp_server.py
echo.
echo 测试完成，请查看上方输出
pause