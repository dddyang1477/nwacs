#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简版飞书指令服务器
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

PORT = 8088

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = """<html><head><meta charset="utf-8"><title>NWACS</title></head>
        <body><h1>NWACS服务器运行中</h1>
        <p>时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p>端口: """ + str(PORT) + """</p></body></html>"""
        self.wfile.write(html.encode('utf-8'))
        print("GET请求来自:", self.client_address)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        print("收到POST:", body[:200])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"code": 0, "msg": "ok"}).encode())

print("="*60)
print("NWACS 极简服务器")
print("="*60)
print(f"端口: {PORT}")
print("按 Ctrl+C 停止")
print()

try:
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"✅ 启动成功! 访问 http://localhost:{PORT}")
    server.serve_forever()
except KeyboardInterrupt:
    print("\n停止")
except Exception as e:
    print(f"错误: {e}")
